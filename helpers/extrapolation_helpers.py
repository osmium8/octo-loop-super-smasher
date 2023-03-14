def get_extrapolated_minutes(tuple):
    if (tuple[1] == 0):
        return 0
    return (tuple[0] / tuple[1]) * 60