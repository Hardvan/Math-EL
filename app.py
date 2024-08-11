from flask import Flask, request, render_template, jsonify
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    # Extract parameters from the form
    params = {
        'N': request.form.get('N', type=int),
        'm': request.form.get('m', type=float),
        'l': request.form.get('l', type=float),
        'g': request.form.get('g', type=float),
        'diameter': request.form.get('diameter', type=float),
        'diameterInfluence': request.form.get('diameterInfluence', type=float),
        'pipeLength': request.form.get('pipeLength', type=float),
        'shotsNumber': request.form.get('shotsNumber', type=int),
        'dt': request.form.get('dt', type=float),
        'ct': request.form.get('ct', type=float)
    }

    # Path to save the new start.m file
    filepath = 'new_start.m'

    # Create the new start.m file
    with open(filepath, 'w') as file:
        file.write(f"""
clc;
clear
%% ============================= Parameters ===============================
% Snake robot parameters 
param.N  = {params['N']};                                      % Number of snake robot links
param.m  = {params['m']};                                   % Weight of snake robot link
param.l  = {params['l']};                                  % Radius of snake robot link
param.g  = {params['g']};                                    % Gravitational acceleration
param.diameter = {params['diameter']};                              % Diameter of a pipeline
param.diameterInfluence = {params['diameterInfluence']};                     % Auxiliary constant
pipeLength = {params['pipeLength']};                                     % Length of a pipeline
param.d = param.diameter - 2*param.l;               % Theoretical diameter for snake robot links
shotsNumber = {params['shotsNumber']};                                   % Auxiliary variable for animation
param.dt = {params['dt']};                                    % Time increment [s]
% Friction coefficients:
param.ct = {params['ct']};                                   % Viscous friction coefphicient of a ground in tangental direction
param.cn = 0.03;                                    % Viscous friction coefphicient of a ground in normal direction
param.ut = 0.15;                                    % Coulomb friction coefphicient of a ground in tangental direction
param.un = 0.3;                                     % Coulomb friction coefphicient of a ground in normal direction
param.ctPipe = 0.08;                                % Viscous friction coefphicient of a pipeline in tangental direction
param.utPipe = 0.2;                                 % Coulomb friction coefphicient of a pipeline in tangental direction
param.umax = 3;                                     % Maximum snake robot link torque
param.qmax = 400*param.dt;                          % Contact parameter
param.Erub = 400000;                                % Contact parameter
param.vrub = 0.49;                                  % Contact parameter                        
param.friction = 1;                                 % Choice of friction:   0 - Coulomb, 1 - viscous
param.contact = 1;                                  % Choice of side walls contact: 0 - without contact, 1 - with contact
param.minLinkVel = 0.001;                           % Auxiliary variable of snake robot link angular velocity
param.dimensionPlot3D = 0;                          % Choice of a graph:    0 - 2D, 1 - 3D
param.resultsShow = 0;                              % Choice of animation:  0 - show simulation, 1 - show graphs 
% Controler parameters:
param.kp  = 25;                                     % Gain for position controller
param.kd  = 10;                                     % Gain for velocity controller
% Simulation time:
t=0:param.dt:20;

%% Initial values for trajectory

% Reference trajectory parameters:
param.alphaA = 0.3981;
param.omega = 0.6936;
param.delta = 0.4914;
param.offset = 0;

% Trajectory
for i=1:param.N-1
    phi = param.alphaA*sin((param.omega*t+(i-1)*param.delta));
    phi_required{{i}} = phi;
    phi_reference(i) = phi(1);
end

% Initial values
theta       = zeros(param.N,1);
thetaDot    = zeros(param.N,1);
phi         = zeros(1,param.N-1); 
phiDot      = zeros(param.N-1,1);
p           = zeros(2,1);
pDot        = zeros(2,1);
qa          = phi';
qu          = [theta(param.N);p(1);p(2)];
qaDot       = phiDot;
quDot       = [thetaDot(param.N);pDot(1);pDot(2)];
x0          = [qa;qu;qaDot;quDot];

%% Solution

[T,X] = ode45(@(t,y)dynamicModel(t,y,param),t,x0);
        """)

    return jsonify({'message': 'File created successfully!'}), 200


if __name__ == '__main__':
    app.run(debug=True)
