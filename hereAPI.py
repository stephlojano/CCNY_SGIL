import requests # for here API requests 
import json
import urllib
import os 
from pandas import DataFrame
import numpy as np
from tqdm import tqdm 

class hereAPI:
    def __init__(self, credentials):
        '''Initializes a hereAPI object that contains creditials required to access Here API'''
        self._webtoken = credentials['webtoken']
        self._secretKey = credentials['secretKey']
        self._apiTag = credentials['apiTag']

        self._cost_matrix = []
        self._distance_matrix = []
        self._duration_matrix = []
        self._energy_matrix = []
        self._polylines = []

    def build_energy_consumption(self, speeds, speed_consump):
        evField = ''
        for i in range(len(speeds)):
            evField += f'{speeds[i]},{speed_consump[i]},'

        return evField[:-1]

    def build_matrices(self, cost_function, charging_stations, vehicle_locations, energy_consumption, time=None, confirm_build=True, roadblocks=None, roadblock_penalty=100e3):
        self.charging_stations = [loc for loc in charging_stations]
        self.vehicle_locations = [loc for loc in vehicle_locations]
        self._cost_matrix = []
        self._distance_matrix = []
        self._duration_matrix = []
        self._energy_matrix = []
        self._polylines = []

        self.roadblocks = None
        if roadblocks:
            self.roadblocks = [loc_pairs for loc_pairs in roadblocks]
        
        row_count = 0
        N_CS = 0
        if confirm_build:
            input(f'You are about to call here API to make {len(vehicle_locations)} x {len(charging_stations)} ({len(charging_stations)*len(vehicle_locations)}) requests. Press enter to continue.')
        print(f"Calling here API for {len(vehicle_locations)} x {len(charging_stations)} ({len(charging_stations)*len(vehicle_locations)}) requests.")
        for origin in tqdm(vehicle_locations, ascii=True, desc=f'Progress '):
            self._cost_matrix.append([])
            self._distance_matrix.append([])
            self._duration_matrix.append([])
            self._energy_matrix.append([])
            self._polylines.append([])
            for destination in charging_stations:
                violated_avoidance = False
                response = self._make_API_request(origin, destination, energy_model=energy_consumption, roadblocks=self.roadblocks,time=time)

                num_sections = len(response['routes'][0]['sections'])
                for span in response['routes'][0]['sections']:
                    if "notices" in span.keys():
                        violated_avoidance = True

                distance = response['routes'][0]['sections'][0]['summary']['length']
                self._distance_matrix[row_count].append(distance)

                duration = response['routes'][0]['sections'][0]['summary']['duration']
                if violated_avoidance:
                    duration *= 100e3
                self._duration_matrix[row_count].append(duration)

                energy_consump = response['routes'][0]['sections'][0]['summary']['consumption']
                self._energy_matrix[row_count].append(energy_consump)

                polyline = response['routes'][0]['sections'][0]['polyline']
                self._polylines[row_count].append(polyline)

                cost = cost_function(N_CS, distance, duration, energy_consump)
                self._cost_matrix[row_count].append(cost)
            row_count += 1
        print('Matrices are ready')

    def get_cost_matrix(self):
        if not self._cost_matrix:
            warn("Cost matrix is empty. Did you build it using .build_matrices method?")
        return self._cost_matrix

    def get_distance_matrix(self):
        if not self._distance_matrix:
            warn("Distance matrix is empty. Did you build it using .build_matrices method?")
        return self._distance_matrix

    def get_duration_matrix(self):
        if not self._duration_matrix:
            warn("Duration matrix is empty. Did you build it using .build_matrices method?")
        return self._duration_matrix

    def get_energy_matrix(self):
        if not self._energy_matrix:
            warn("Energy matrix is empty. Did you build it using .build_matrices method?")
        return self._energy_matrix

    def get_polylines(self):
        if not self._polylines:
            warn("No polylines found. Did you build it using .build_matrices method?")
        return self._polylines

    def check_credentials(self):
        testorg = (40.667864, -73.994026)
        testdest = (40.678123, -73.990967)
        api_origin = f'&origin={testorg[0]},{testorg[1]}'
        api_dest = f'&destination={testdest[0]},{testdest[1]}'
        here_api_request = f'https://router.hereapi.com/v8/routes?transportMode=car{api_origin}{api_dest}&return=summary,polyline{self._apiTag}'
        response = requests.get(here_api_request).json()
        if 'error' in response.keys():
            from warnings import warn
            warn('Check your Here API Credentials. Please visit: https://developer.here.com/documentation/authentication/dev_guide/index.html')
        else:
            print('Credentials OK')

    def cache_cost_matrix(self, cost_matrix=None, run_tag='', target_dir=None):
        if not target_dir:target_dir = 'data_cache'

        if not os.path.isdir(f'./{target_dir}'):
            os.mkdir(f'{target_dir}')

        # filename = os.path.join('data_cache', filename)
        if not cost_matrix:
            DataFrame(np.array(self._cost_matrix)).to_csv(os.path.join(target_dir, f'{run_tag}-cost_mat.csv'))
        else:
            DataFrame(np.array(cost_matrix)).to_csv(os.path.join(target_dir, f'{run_tag}-cost_mat.csv'))
        if run_tag: print(f'Matrices saved in {target_dir} directory with run tag: {run_tag}')
        else: print(f'Matrices saved in {target_dir} directory.')
    
    def cache_matrices(self, run_tag='', target_dir=None):
        if not target_dir:target_dir = 'data_cache'

        if not os.path.isdir(f'./{target_dir}'):
            os.mkdir(f'{target_dir}')

        # filename = os.path.join('data_cache', filename)
        DataFrame(np.array(self._cost_matrix)).to_csv(os.path.join(target_dir, f'{run_tag}-cost_mat.csv'))
        DataFrame(np.array(self._distance_matrix)).to_csv(os.path.join(target_dir, f'{run_tag}-dist_mat.csv'))
        DataFrame(np.array(self._duration_matrix)).to_csv(os.path.join(target_dir, f'{run_tag}-dur_mat.csv'))
        DataFrame(np.array(self._energy_matrix)).to_csv(os.path.join(target_dir, f'{run_tag}-energy_mat.csv'))
        DataFrame(np.array(self._polylines)).to_csv(os.path.join(target_dir, f'{run_tag}polylines.csv'))
        if run_tag: print(f'Matrices saved in {target_dir} directory with run tag: {run_tag}')
        else: print(f'Matrices saved in {target_dir} directory.')

    def _make_API_request(self,origin, destination, energy_model=None, roadblocks=None, time=None):
        assert(isinstance(roadblocks, type(None)) or isinstance(roadblocks, list))
        api_origin = f'&origin={origin[0]},{origin[1]}'
        api_dest = f'&destination={destination[0]},{destination[1]}'
        avoid = ''
        evField = ''
        
        if roadblocks: avoid = self._compile_roadblocks(roadblocks)
        if energy_model: evField = self._compile_energy_model(energy_model)
        if time: time = '&departureTime=' + time

        here_api_request = f'https://router.hereapi.com/v8/routes?transportMode=car{api_origin}{api_dest}{time}{evField}{avoid}&return=summary,polyline,travelSummary,actions,instructions{self._apiTag}'

        response = requests.get(here_api_request)
        return response.json()

    def _compile_energy_model(self, energy_speed_model):
        energy_consumption_field = '&ev[freeFlowSpeedTable]='

        for element in energy_speed_model:
            energy_consumption_field += f'{element},'
        return energy_consumption_field[:-1]
        

    def _compile_roadblocks(self, bounding_boxes):
        roadblock = '&avoid[areas]='
        for box in bounding_boxes:
            roadblock += f'bbox:{box[0][0]},{box[0][1]},{box[1][0]},{box[1][1]}|'
        return roadblock[:-1]

    