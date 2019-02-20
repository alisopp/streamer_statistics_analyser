import datetime
import math
import random

colors = [  # from https://sashat.me/2017/01/11/list-of-20-simple-distinct-colors/
    "#e6194b", "#3cb44b", "#ffe119", "#0082c8", "#f58231", "#911eb4", "#46f0f0", "#f032e6",
    "#d2f53c", "#fabebe", "#008080", "#e6beff", "#aa6e28", "#fffac8", "#800000", "#aaffc3",
    "#808000", "#ffd8b1", "#000080", "#808080", "#000000"
]

amplitudes = [0.2]  # , 0.5, 1.0, 0.7, 0.5, 0.4]
frequencies = range(1, 31)  # , 2, 4, 8, 16, 32]


def weighted_sum(amplitudes, noises, mapsize, avg):
    output = [0.0] * mapsize  # make an array of length mapsize
    for k in range(len(noises)):
        for x in range(mapsize):
            output[x] += int(((amplitudes[k] * noises[k][x])) * avg)
    return output


def noise(freq, mapsize):
    phase = random.uniform(0, 2 * math.pi)
    return [math.sin(2 * math.pi * freq * x / mapsize + phase) + 1
            for x in range(mapsize)]


def smoother(noise):
    output = []
    for i in range(len(noise) - 1):
        next_number = 0.5 * (noise[i] + noise[i + 1])
        output.append(next_number)
    return output


def generate_smooth_noise(seed, mapsize):
    random.seed(seed)
    noise = [random.uniform(0, +1) for i in range(mapsize)]
    x = []
    for i in range(0, mapsize - 1):
        x.append(i)
    return (x, smoother(noise))


def generate_combined_noise(mapsize):
    for i in range(1):
        random.seed(i)
        noises = [noise(f, mapsize) for f in frequencies]
        sum_of_noises = weighted_sum(amplitudes, noises, mapsize, 50000)


def random_ift(amplitude, mapsize, avg):
    amplitudes = [amplitude(f) for f in frequencies]
    noises = [noise(f, mapsize) for f in frequencies]
    sum_of_noises = weighted_sum(amplitudes, noises, mapsize, avg)
    return sum_of_noises


def generate_fake_data(seed, start_date=datetime.datetime.utcnow(), end_date=datetime.datetime.utcnow(),
                       languages=["ger", "en"]):
    random.seed(seed)
    time_diff = int(((end_date - start_date).total_seconds() / 60.0) / 5)
    json_dict = {}
    json_dict['chart_data'] = []
    currentColor = 0
    for lang in languages:
        chart_data = {}
        y1 = random_ift(lambda f: float(5.0 / f), time_diff, random.randint(500, 1000))
        chart_data['fill'] = False
        chart_data['backgroundColor'] = colors[currentColor]
        chart_data['borderColor'] = colors[currentColor]
        chart_data['data'] = y1
        chart_data['label'] = lang
        currentColor += 1
        json_dict['chart_data'].append(chart_data)
    json_dict['observation_date'] = []
    json_dict["title_sub"] = start_date.strftime("%Y.%m.%d") + " - " + end_date.strftime("%Y.%m.%d")
    for x in range(0, time_diff - 1):
        current_time = start_date + datetime.timedelta(0, 0, 0, 0, 5 * x)
        json_dict['observation_date'].append(current_time.strftime("%Y.%m.%d %H:%M"))
    return json_dict
