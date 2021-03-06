classdef robot_class
    %ROBOT Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        Name % Name of the robot
        Obstacle %  Give booleans if obstacles place on the front/back/left/right
        Scan % raw data from the LIDAR
        
        Map %  matrix filled with 0 or 1 representing the map
        Waypoints % All the points to achieve goals
        Command % Command order to send to the robot
        
        Action % l'action en cours
        
    end
    
    methods
        function obj = robot_class(name)
            %ROBOT Construct an instance of this class
            obj.Name = name;
            obj.Obstacle = obstacle_class();
        end

        function bool = is_obstacle(obj,position)
            %ROBOT Construct an instance of this class
            if position == "devant"
                bool = obj.Obstacle.Front;
            end
            if position == "derriere"
                bool = obj.Obstacle.Back;
            end
            if position == "droite"
                bool = obj.Obstacle.Right;
            end
            if position == "gauche"
                bool = obj.Obstacle.Left;
            end
        end

    end
end

