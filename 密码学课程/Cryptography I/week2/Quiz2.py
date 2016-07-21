def main():
    price_per_pc = 200
    brute_force_speed_per_pc_second = 10 ** 9
    budget = 4 * (10 ** 12)
    total_cipher = 2 ** 128
    amount_mechines = budget / price_per_pc
    time = total_cipher / (amount_mechines * brute_force_speed_per_pc_second)
    format_time(time)


def format_time(time):
    dictionary = {}
    dictionary["time_seconds"] = time
    dictionary["time_minutes"] = dictionary["time_seconds"] / 60
    dictionary["time_hours"] = dictionary["time_minutes"] / 60
    dictionary["time_days"] = dictionary["time_hours"] / 24
    dictionary["time_months"] = dictionary["time_days"] / 30
    dictionary["time_years"] = dictionary["time_months"] / 12
    dictionary["time_billion_years"] = dictionary["time_years"] / (10 ** 9)

    for key, value in dictionary.items():
        print("{0} = {1}".format(key, value))
