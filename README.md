Modify a gslib file by:
    - Adding offsets to i_index, j_index, k_index
    - Keeping x_coord, y_coord, z_coord unchanged
    - Removing extra columns
    - Adding 4 new columns: dip_angle, strike_angle, KN, KS

    Parameters:
    -----------
    input_file : str
        Path to the input gslib file
    output_file : str
        Path to the output gslib file
    i_offset : int
        Constant to add to i_index
    j_offset : int
        Constant to add to j_index
    k_offset : int
        Constant to add to k_index
    dip_angle : float or list
        Constant value(s) for dip_angle column
    strike_angle : float or list
        Constant value(s) for strike_angle column
    KN : int or list
        Constant value(s) for KN column
    KS : int or list
        Constant value(s) for KS column
