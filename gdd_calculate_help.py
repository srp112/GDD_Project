def calculate_gdd ( temp, tbase=10, tmax=40 ):
    """This function calculates the Growing Degree Days for a given year from
    the ERA Interim daily mean surface temperature data. The user can select a 
    base temperature in degrees Celsius. By default, the value is 10. If no
    year is specified, the whole time series is retrieved. Note that if you 
    don't specify time and location, the operation can be quite slow and will
    return lots of data."""
    
    if temp.ndim == 3:
        b = np.clip ( temp, tbase, tmax )
        c = np.where ( b-tbase<0, 0, b-tbase )
        agdd = c.cumsum (axis=0)
    else:


        if temp.shape[0] <= 367:
            # Only one year of data
            b = np.clip ( temp, tbase, tmax )
            c = np.where ( b-tbase < 0, 0, b-tbase )
            agdd = c.cumsum ( axis=0 )
        else:
            b = np.clip ( temp, tbase, tmax )
            c = np.where ( b-tbase < 0, 0, b-tbase )
            agdd = np.zeros( 4017 )
            for y in xrange ( 11 ):
                a = c[y*365:(y+1)*365]
                o = a.cumsum ( axis=0)
                agdd[y*365:(y+1)*365] = o
    return agdd

