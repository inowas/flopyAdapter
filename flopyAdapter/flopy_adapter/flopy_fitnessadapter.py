"""
Calculation of objective values of a datamodel

Author: Aybulat Fatkhutdinov / Benjamin Gutzmann
"""

import os
import pathlib
import math
import numpy as np
from typing import Union
import flopy


class FlopyFitnessAdapter:
    """Calculation of objective values of a datamodel

    Args:
        objectives () -
        constraints () -
        objects () -
        flopy_adapter () -

    """

    def __init__(self,
                 objectives: list,
                 constraints: list,
                 objects: list,
                 flopy_adapter: flopy.modflow.Modflow):

        self.objectives = objectives
        self.constraints = constraints
        self.objects = objects
        # self.optimization_data = optimization_data

        self.dis_package = flopy_adapter.get_package('DIS')  # _mf.
        self.model_ws = flopy_adapter.model_ws  # _mf.
        self.model_name = flopy_adapter.namefile.split('.')[0]  # _mf.
        # self.objects = self.optimization_data['objects']

    @staticmethod
    def from_data(objectives: list,
                  constraints: list,
                  objects: list,
                  flopy_adapter: flopy.modflow.Modflow):
        if not isinstance(objectives, list):
            raise TypeError(f"Error: objectives is of type {type(objectives)}, should be of type list.")
        if not isinstance(constraints, list):
            raise TypeError(f"Error: constraints is of type {type(constraints)}, should be of type list.")
        if not isinstance(objects, list):
            raise TypeError(f"Error: objects is of type {type(objects)}, should be of type list.")
        if not isinstance(flopy_adapter, flopy.modflow.Modflow):
            raise TypeError(f"Error: flopy_adapter is of type {type(flopy_adapter)}, should be Modflow object.")

        return FlopyFitnessAdapter(objectives, constraints, objects, flopy_adapter)

    def get_fitness(self):
        objectives_values = self.read_objectives()
        constraints_exceeded = self.check_constraints()

        if True in constraints_exceeded or None in objectives_values:
            fitness = [obj["penalty_value"] for obj in self.objectives]
        else:
            fitness = objectives_values

        return fitness

    def read_objectives(self):
        """Returns fitness list

        Args:
            self - holds constraints

        Returns:


        """

        fitness = []

        for objective in self.objectives:
            value = None

            if objective["type"] == "concentration":
                mask = self.make_mask(
                    objective["location"], self.objects, self.dis_package
                )
                value = self.read_concentration(objective, mask, self.model_ws, self.model_name)

            elif objective["type"] == "head":
                mask = self.make_mask(
                    objective["location"], self.objects, self.dis_package
                )
                value = self.read_head(objective, mask, self.model_ws, self.model_name)

            elif objective["type"] == "flux":
                value = self.read_flux(objective, self.objects)

            elif objective["type"] == "input_concentration":
                value = self.read_input_concentration(objective, self.objects)

            # if not value:
            #     print(f"Error: could not read objective for {objective['type']}.")
            
            value = self.summary(value, objective["summary_method"])
            fitness.append(value.item())

        return fitness
    
    def check_constraints(self):
        """Checks constraints

        Args:
            self - holds constraints

        Returns:


        """

        constraints_exceeded = []

        for constraint in self.constraints:
            value = None

            if constraint["type"] == 'head':
                mask = self.make_mask(
                    constraint["location"], self.objects, self.dis_package    
                )
                value = self.read_head(
                    constraint, mask, self.model_ws, self.model_name
                )
   
            elif constraint["type"] == 'concentration':
                mask = self.make_mask(
                    constraint["location"], self.objects, self.dis_package    
                )
                value = self.read_concentration(
                    constraint, mask, self.model_ws, self.model_name
                )
            
            elif constraint["type"] == "flux":
                value = self.read_flux(
                    constraint, self.objects
                )
            
            elif constraint["type"] == "input_concentrations":
                value = self.read_input_concentration(
                    constraint, self.objects
                )
            
            value = self.summary(value, constraint["summary_method"])
            
            if constraint["operator"] == "less":
                if value > constraint["value"]:
                    print(f"Constraint value {value} exceeded max value {constraint['value']}, penalty will be assigned")
                    constraints_exceeded.append(True)
                else:
                    constraints_exceeded.append(False)
                
            elif constraint["operator"] == "more":
                if value < constraint["value"]:
                    print(f"Constraint value {value} lower than min value {constraint['value']}, penalty will be assigned")
                    constraints_exceeded.append(True)
                else:
                    constraints_exceeded.append(False)

        return constraints_exceeded
    
    @staticmethod
    def summary(result, method):
        """Reads head file

        Args:
            result () -
            method () -

        Returns:


        """

        if method == 'mean':
            result = np.nanmean(result)
        elif method == 'max':
            result = np.max(result)
        elif method == 'min':
            result = np.min(result)
        else:
            print(f"Unknown summary method {method}. Using max")
            result = np.max(result)
        
        return result

    @staticmethod
    def read_head(data, mask, model_ws, model_name):
        """Reads head file

        Args:
            data () -
            mask () -
            model_ws () -
            model_name () -

        Returns:


        """

        print(f'Read head values at location: {data["location"]}')
        
        try:
            print(f"{pathlib.Path(model_ws, model_name)}.hds")

            head_file_object = flopy.utils.HeadFile(
                f"{pathlib.Path(model_ws, model_name)}.hds", verbose=True)

            print("Read head.")

            head = head_file_object.get_alldata(
                nodata=-9999
                )
            head = head[mask]

            head_file_object.close()

            return head
        except FileNotFoundError:
            print(f'Head file of the datamodel: {model_name} not found')
        except Exception as e:
            print(f'Head file of the datamodel: {model_name} could not be opened'
                  f"{str(e)}")

        return
    
    @staticmethod
    def read_concentration(data, mask, model_ws, model_name):
        """Reads concentrations file

        Args:
            data () -
            mask () -
            model_ws () -
            model_name () -

        Returns:


        """

        print(f'Read concentration values at location: {data["location"]}')

        try:
            print(os.path.join(model_ws, data["conc_file_name"]))
            conc_file_object = flopy.utils.UcnFile(
                os.path.join(model_ws, data["conc_file_name"]))
            conc = conc_file_object.get_alldata(
                nodata=-9999
                )
            conc = conc[mask]

            conc_file_object.close()

            return conc
        except FileNotFoundError:
            print(f'Concentration file of the datamodel: {model_name} not found')
        except Exception as e:
            print(f'Concentration file of the datamodel: {model_name} could not be opened'
                  f"{str(e)}")

        return
    
    @staticmethod
    def read_flux(data, objects):
        """Reads wel fluxes

        Args:
            data () -
            objects () -

        Returns:


        """

        print(f'Read flux values at location: {data["location"]}')

        fluxes = np.array([])

        try:
            obj_ids = data["location"]["objects"]
        except KeyError:
            print("Error: Objective location of type Flux has to be an Object!")
            return None

        for obj in objects:
            if obj['id'] in obj_ids:
                obj_fluxes = []
                for period_data in obj['flux'].values():
                    obj_fluxes.append(period_data['result'])
        
                fluxes = np.hstack((fluxes, np.array(obj_fluxes)))

        return fluxes
    
    @staticmethod
    def read_input_concentration(data, objects):
        """Reads wel fluxes

        Args:
            data () -
            objects () -

        Returns:


        """

        print(f'Read input_concentration values at location: {data["location"]}')

        input_concentrations = np.array([])

        try:
            component = data["component"]
        except KeyError:
            print("ERROR! Concentration component for the Objective of type input_concentrations is not defined!")
            return None
        
        try:
            obj_ids = data["location"]["objects"]
        except KeyError:
            print("ERROR! Objective location of type input_concentrations has to be an Object!")
            return None
        
        for obj in objects:
            if obj['id'] in obj_ids:
                obj_concentrations = []
                for period_data in obj['concentration'].values():
                    obj_concentrations.append(period_data[component]['result'])
                input_concentrations = np.hstack((input_concentrations, np.array(obj_concentrations)))

        return input_concentrations
    
    @staticmethod
    def read_distance(data, objects):
        """Returns distance between two groups of objects

        Args:
            data () -
            objects () -

        Returns:


        """

        print(f'Read distance between {data["location_1"]} and {data["location_2"]}')

        location_1 = data["location_1"]
        location_2 = data["location_2"]
        
        objects_1 = None
        objects_2 = None

        if location_1['type'] == 'object':
            objects_1 = [
                obj for id_, obj in objects.items() if id_ in location_1['objects_ids']
            ]

        if location_2['type'] == 'object':
            objects_2 =[
                obj for id_, obj in objects.items() if id_ in location_2['objects_ids']
            ]
        
        distances = []
        if objects_1 is not None:
            for obj_1 in objects_1:
                if objects_2 is not None:
                    for obj_2 in objects_2:
                        dx = float(abs(obj_2['position']['col']['result'] - obj_1['position']['col']['result']))
                        dy = float(abs(obj_2['position']['row']['result'] - obj_1['position']['row']['result']))
                        dz = float(abs(obj_2['position']['lay']['result'] - obj_1['position']['lay']['result']))
                        distances.append(math.sqrt((dx**2) + (dy**2) + (dz**2)))
                else:
                    dx = float(abs(location_2['lay_row_col'][2] - obj_1['position']['col']['result']))
                    dy = float(abs(location_2['lay_row_col'][1] - obj_1['position']['row']['result']))
                    dz = float(abs(location_2['lay_row_col'][0] - obj_1['position']['lay']['result']))
                    distances.append(math.sqrt((dx**2) + (dy**2) + (dz**2)))
        else:
            if objects_2 is not None:
                for obj_2 in objects_2:
                    dx = float(abs(obj_2['position']['col']['result'] - location_1['lay_row_col'][2]))
                    dy = float(abs(obj_2['position']['row']['result'] - location_1['lay_row_col'][1]))
                    dz = float(abs(obj_2['position']['lay']['result'] - location_1['lay_row_col'][0]))
                    distances.append(math.sqrt((dx**2) + (dy**2) + (dz**2)))
            else:
                dx = float(abs(location_2['lay_row_col'][2]-location_1['lay_row_col'][2]))
                dy = float(abs(location_2['lay_row_col'][1]-location_1['lay_row_col'][1]))
                dz = float(abs(location_2['lay_row_col'][0]-location_1['lay_row_col'][0]))
                distances.append(math.sqrt((dx**2) + (dy**2) + (dz**2)))

        distances = np.array(distances)
        
        return distances

    @staticmethod
    def make_mask(location, objects, dis_package):
        """Returns an array mask of location that has nper,nlay,nrow,ncol dimensions

        Args:
            location () -
            objects () -
            dis_package () -

        Returns:


        """

        print(f'Making mask array for location: {location}')
        nstp_flat = dis_package.nstp.array.sum()
        nrow = dis_package.nrow
        ncol = dis_package.ncol
        nlay = dis_package.nlay

        mask = None

        if location["type"] == 'bbox':
            per_min = location.get('per_min', 0)
            per_max = location.get('per_max', nstp_flat)

            lay_min = location.get('lay_min', 0)
            lay_max = location.get('lay_max', nlay)

            col_min = location.get('col_min', 0)
            col_max = location.get('col_max', ncol)

            row_min = location.get('row_min', 0)
            row_max = location.get('row_max', nrow)

            if per_min == per_max:
                per_max += 1
            if lay_min == lay_max:
                lay_max += 1
            if row_min == row_max:
                row_max += 1
            if col_min == col_max:
                col_max += 1
        
            mask = np.zeros((nstp_flat, nlay, nrow, ncol), dtype=bool)
            mask[
                per_min:per_max,
                lay_min:lay_max,
                row_min:row_max,
                col_min:col_max
            ] = True

        elif location["type"] == 'object':
            lays = []
            rows = []
            cols = []
            for obj in objects:
                if obj['id'] in location['objects']:
                    lays.append(obj['position']['lay']['result'])
                    rows.append(obj['position']['row']['result'])
                    cols.append(obj['position']['col']['result'])

            mask = np.zeros((nstp_flat, nlay, nrow, ncol), dtype=bool)
            mask[:, lays, rows, cols] = True
        
        return mask
