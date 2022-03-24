import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class TurningCircle():

    def __init__(self, angle:float, nominal_speed:float,
                lpp:float, df: pd.DataFrame):
        self.df = df
        self.angle = angle
        self.nominal_speed = nominal_speed
        self.lpp = lpp
        self.results = {}

        ## Checks:
        
        mandatorys = ['psi', 
                      'x0',
                      'y0',
                      'r',
                      'u',
                      'v',
                      'V']
        for mandatory in mandatorys:     
            assert f"'{mandatory}' must exist in df"
                
        assert df['delta'].abs().max() < np.deg2rad(90), "'delta should be in radians"

        self.units = {
            'TrackSpeed' : r'm/s',
        }

    @property
    def start(self):
        start = self.df.iloc[0]
        return start

    @property
    def end(self):
        end = self.df.iloc[-1]
        return end

    @property
    def heading_change_90(self):

        start = self.start
        psi_change = self.df['psi'] - start['psi']
        index_90 = (psi_change.abs() > np.deg2rad(90))  # First time ship passes 90 deg
        return self.df.loc[index_90].iloc[0]

    @property
    def heading_change_180(self):

        start = self.start

        psi_change = self.df['psi'] - start['psi']
        index_180 = (psi_change.abs() > np.deg2rad(180))  # First time ship passes 90 deg
        return self.df.loc[index_180].iloc[0]

    @property
    def advance(self):

        s_90 = self.heading_change_90
        start = self.start
        advance = np.abs(s_90['x0'] - start['x0'])
        return advance

    @property
    def transfer(self):

        s_90 = self.heading_change_90
        start = self.start
        transfer = np.abs(s_90['y0'] - start['y0'])
        return transfer

    @property
    def tactical_diameter(self):

        s_180 = self.heading_change_180
        start = self.start
        tactical_diameter = np.abs(s_180['y0'] - start['y0'])
        return tactical_diameter

    @property
    def steady_turning_diameter(self):

        s_180 = self.heading_change_180
        end = self.end

        mask = ((self.df.index >= s_180.name) & (self.df.index <= end.name))
        df = self.df.loc[mask].copy()

        mask = df['r'].abs() != 0
        df = df.loc[mask]
        r = df['r']
        V = df['V']
        R = V/r
        steady_turning_diameter = np.abs(2*R.median())

        return steady_turning_diameter

    def evaluate(self):

        results = {}

        # IMO standard:
        lpp = self.lpp
        V = self.nominal_speed  # [m/s] !!!

        #if self.angle == 35:
        results['initial_speed'] = V
        results['Advance (IMO)'] = 4.5*lpp
        results['Tactical diameter (IMO)'] = 5*lpp

        results['advance'] = self.advance
        results['transfer'] = self.transfer
        results['tactical_diameter'] = self.tactical_diameter
        results['steady_turning_diameter'] = self.steady_turning_diameter

        units = {
            'advance':'m',
            'transfer': 'm',
            'tactical_diameter':'m',
            'steady_turning_diameter':'m',
            'Advance (IMO)':'m',
            'Tactical diameter (IMO)':'m',
            'initial_speed':self.units['TrackSpeed']
        }
        units.update(self.units)
        results['units'] = units

        self.results['turning_circle'] = results

        return results