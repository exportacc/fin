def linear_interpolation(xi,params):
        x1,x2,y1,y2 = params 
        '''
        linear interpolation method

        x1 ：  Lower point on the X-axis
        x2 ：  Higher point on the X-axis
        xi ：  Point on the X-axis to be interpolated (target)
        y1 ：  Lower point on the Y-axis
        y2 ：  Higher point on the Y-axis
        '''
        return ((y2-y1) * ( (xi-x1)/(x2-x1) ) + y1)
