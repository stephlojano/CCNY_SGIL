import pandas as pd 
import numpy as np 
import os 
import json
from .geoutil import decode_polyline, get_distance, within_proximity

class SGIL_solver:
    def __init__(self, cost_function, charging_stations, vehicle_locations, cost_matrix=None,
                distance_matrix=None, duration_matrix=None, energy_matrix=None, polylines=None):
        self.cost_matrix = cost_matrix
        self.distance_matrix = distance_matrix 
        self.duration_matrix = duration_matrix
        self.energy_matrix = energy_matrix
        self.polylines = polylines

        self.charging_stations = {}
        self.vehicle_locations = {}

        # initialize charging_stations dictionary to include N_CS
        for idx, loc in enumerate(charging_stations):
            self.charging_stations[idx] = {
                'location': loc, 
                'N_CS': 0
            } 
        
        # initialize vehicle_locations dict to include vehicle identification nums
        for idx, loc in enumerate(vehicle_locations):
            self.vehicle_locations[idx] = loc 

        self._original_vehicle_locs = self.vehicle_locations

        self.cost_function = cost_function

        self._cached_cost_matrix = cost_matrix
        self._cached_distance_matrix = distance_matrix 
        self._cached_duration_matrix = duration_matrix
        self._cached_energy_matrix = energy_matrix

    def _update_cost_matrix(self, col_num):
        station = list(self.charging_stations.keys())[col_num]
        self.charging_stations[station]['N_CS'] += 1
        N_CS = self.charging_stations[station]['N_CS']

        for row_num in range(len(self.cost_matrix)):
            distance = self.distance_matrix[row_num][col_num]
            duration = self.duration_matrix[row_num][col_num]
            energy = self.energy_matrix[row_num][col_num] 

            new_cost = self.cost_function(N_CS, distance, duration, energy)
            self.cost_matrix[row_num][col_num] = new_cost

    def _decide(self, vehicle_num):
        # station_names = list(self.charging_stations.keys())
        # print(f"Deciding for {vehicle_num}")
        min_cost = min(self.cost_matrix[vehicle_num])
        # print(f"\t min_cost = {min_cost}")
        min_idx = self.cost_matrix[vehicle_num].index(min_cost)
        # print(f"\t Index = {min_idx} | length of cost matrix is: {len(self.cost_matrix[vehicle_num])}")
        return min_cost, min_idx

    def load_data_from_cache(self, run_tag='', cache_dir='data_cache'):
        assert (os.path.isdir(cache_dir)),"data_cache DIRECTORY NOT FOUND - data could not be loaded."
        self.cost_matrix = np.delete(pd.read_csv('cost_mat.csv').to_numpy(), obj=0, axis=1).tolist()
        self.distance_matrix = np.delete(pd.read_csv('dist_mat.csv').to_numpy(), obj=0, axis=1).tolist()
        self.duration_matrix = np.delete(pd.read_csv('dur_mat.csv').to_numpy(), obj=0, axis=1).tolist()
        self.energy_matrix = np.delete(pd.read_csv('en_mat.csv').to_numpy(), obj=0, axis=1).tolist()
        self.polylines = np.delete(pd.read_csv('polylines.csv').to_numpy(), obj=0, axis=1).tolist()

    def solve(self, cost_matrix=None, distance_matrix=None, duration_matrix=None, energy_matrix=None, polylines=None, order=None, random_order=True, hereAPI=None, cache_tag=None, cache_dir=None):
        if cost_matrix: self.cost_matrix = cost_matrix
        if distance_matrix: self.distance_matrix = distance_matrix 
        if duration_matrix: self.duration_matrix = duration_matrix
        if energy_matrix: self.energy_matrix = energy_matrix
        if polylines: self.polylines = polylines
        if hereAPI: self.hereAPI = hereAPI
        if not cache_tag: cache_tag = ''

        num_vehicles = len(self.vehicle_locations.keys())
        self.solution = {}

        if random_order and not order:
            order = list(self.vehicle_locations.keys())
            np.random.shuffle(order)
            
        elif not order:
            order = list(self.vehicle_locations.keys())
            
        print("Solving in the following order:")
        print(order)
        count = 0
        for vehicle_num in order:
            charging_cost, charging_station_idx = self._decide(vehicle_num)
            # print(f"trying to access self.charging_station[{charging_station_idx}]")
            self._update_cost_matrix(charging_station_idx)
            # print(type(vehicle_num), type(charging_station_idx), type(self.solution))
            if hereAPI: hereAPI.cache_cost_matrix(self.cost_matrix, run_tag=f'{cache_tag}_vehice{count}', target_dir=cache_dir)
            self.solution[vehicle_num] = {
                    'polyline' : self.polylines[vehicle_num][charging_station_idx],
                    'station' : charging_station_idx
                }
            count += 1
        return self.solution

    def compare_solutions(self, alternate_solution):
        differences = {}
        for key, value in self.solution.items():
            if value != alternate_solution[key]:
                differences[key] = {
                    'Current soluion': value, 
                    'Alternate Solution' : alternate_solution[key]
                }
        if len(differences) == 0:
            print("No changes in the solution!")
        return differences
    
    def get_nodal_route(self, vehicle_number, nodal_map, polylines=None, solution=None):
        if not solution: 
            solution = self.solution

        if not polylines: 
            polylines = self.polylines

        charging_station = solution[vehicle_number]['station']
        polyline = polylines[vehicle_number][charging_station]

        
        coordinates = decode_polyline(polyline)
        route = []
        for coordinate in coordinates:
            for node_num, node_loc in nodal_map.items():
                if within_proximity(coordinate, node_loc) and node_num != route[-1]:
                    route.append(node_num)

        return route

    def convert_polyline_to_route(self, polyline, nodal_map):
        coordinates = decode_polyline(polyline)
        route = []
        for coordinate in coordinates:
            for node_num, node_loc in nodal_map.items():
                if within_proximity(coordinate, node_loc) and node_num not in route:
                    route.append(node_num)
        return route


    def print_nodal_route(self, route):
        for i in range(len(route) -1):
            if route[i] != route[i+1]:
                print(f"{route[i]} -> ", end='')

        print(f"{route[-1]}")

    def print_nodal_routes(self, routes):
        for vehicle, route in routes.items():
            print(f"vehicle #{vehicle} : ")
            self.print_nodal_route(route)

    def get_all_nodal_routes(self, nodal_map, polylines=None, solution=None):
        all_routes = {}
        if not solution: 
            solution = self.solution
        if not polylines:
            polylines = self.polylines

        for vehicle in solution.keys():
            all_routes[vehicle] = self.get_nodal_route(vehicle, polylines, nodal_map)

        return all_routes

    def reset(self):
        self.cost_matrix = self._cached_cost_matrix
        self.distance_matrix = self._cached_distance_matrix
        self.duration_matrix = self._cached_distance_matrix
        self.energy_matrix = self._cached_energy_matrix

    def cache_solution(self,soluion, tag):
        filename=f"solution{tag}.json"
        with open(os.path.join('exp_results',filename), 'w') as fp:
            json.dump(solution, fp)

    def experiment(self, hereAPI, cost_function, gowanus_CS, vehicle_locations, energy_consumption_model, roadblocks, time, order=None, random_order=True, num_experiments=None):
        if not num_experiments:
            num_experiments = {'no roadblocks': 1, 'roadblocks': 1} # default split 

        experiment_solutions = []
        for i in range(sum(num_experiments.values())):
            if i < int(num_experiments['no roadblocks']):
                hereAPI.build_matrices(cost_function, gowanus_CS, vehicle_locations, energy_consumption_model, time=time, confirm_build=False)
            else:
                hereAPI.build_matrices(cost_function, gowanus_CS, vehicle_locations, energy_consumption_model, time=time,
                         roadblocks=roadblocks, confirm_build=False)

            cost_matrix = hereAPI.get_cost_matrix()
            distance_matrix = hereAPI.get_distance_matrix()
            duration_matrix = hereAPI.get_duration_matrix()
            energy_matrix = hereAPI.get_energy_matrix()
            polylines = hereAPI.get_polylines() 

            solution = self.solve(cost_matrix=cost_matrix, distance_matrix=distance_matrix, duration_matrix=duration_matrix, energy_matrix=energy_matrix, polylines=polylines,
                                    order=order, random_order=random_order)
            
            experiment_solutions.append(solutions)
            self.cache_solution(solution, i)
        return experiment_solutions
                

    

        
    



