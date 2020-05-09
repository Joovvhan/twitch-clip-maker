import argparse
import os
import glob
import re

from collections import namedtuple
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import itertools

Chat = namedtuple('Chat', 'time id text')

def load_chat(log_file):

    t0 = datetime.strptime('00:00:00', '%H:%M:%S')

    chat_history = list()

    with open(log_file, 'r') as file:
        for chat in file:
            chat_time = re.search('\[.*?\]', chat)[0]
            user_id_match = re.search('<.*?>', chat)
            user_id = user_id_match[0]
            start_of_chat = user_id_match.span()[-1]
            text = chat[start_of_chat:].strip()

            dt = datetime.strptime(chat_time, '[%H:%M:%S]') - t0
            chat_tuple = Chat(dt.total_seconds(), user_id[1:-1], text)

            chat_history.append(chat_tuple)

    return chat_history

def express_bins_as_time_range(bins, index_list):

    # time_range_list = list()
    time_range_string_list = list()

    for index in index_list:
        begin = timedelta(seconds=int(bins[index]))
        end = timedelta(seconds=int(bins[index + 1]))
        # print('[{} ~ {}]\n'.format(begin, end))
        time_range_string_list.append('[{} ~ {}]'.format(begin, end))
        # time_range_list.append((begin, end))

    return time_range_string_list

def plot_chat_time_histogram(chat_time_list, segment_duration, moving_average_duration, sigma):

    num_bins = np.int(np.ceil(max(chat_time_list) / segment_duration))

    # histogram, bins, _ = plt.hist(chat_time_list, bins=num_bins)

    histogram, bins = np.histogram(chat_time_list, bins=num_bins, density=False)

    mov_avg_window_len_float = moving_average_duration / segment_duration

    mov_avg_window_len = int(mov_avg_window_len_float)

    if mov_avg_window_len_float != mov_avg_window_len:
        print('[ W ] [ mov_avg_window_len_float / mov_avg_window_len | {} / {} ]'.format(mov_avg_window_len_float, mov_avg_window_len))

    historgram_avg = np.convolve(histogram, np.ones(mov_avg_window_len) / mov_avg_window_len, 'same')

    histogram_delta = histogram - historgram_avg

    outlier_idx = np.argwhere(histogram_delta > np.mean(histogram_delta) + sigma * np.std(histogram_delta))
    outlier_idx = list(itertools.chain.from_iterable(outlier_idx))

    # print(outlier_idx)
    time_range_string_list = express_bins_as_time_range(bins, outlier_idx)

    plt.figure(figsize=(18, 6))
    plt.plot(bins[:-1], histogram)
    plt.plot(bins[:-1], historgram_avg)
    plt.plot(bins[:-1][outlier_idx], histogram[outlier_idx], '*')
    plt.show()

    return time_range_string_list

    # plt.figure()
    # _, _, _ = plt.hist(histogram_delta, bins=20)
    # plt.show()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', type=str, help='twitch video id')
    parser.add_argument('--log_folder', type=str, help='twitch log folder', default='chats')
    parser.add_argument('--sigma', type=float, help='outlier criterion', default=3)
    parser.add_argument('--output_folder', type=str, help='result folder', default='results')
    parser.add_argument('--segment_duration', type=int, help='segment duration in seconds', default=60)
    parser.add_argument('--mov_avg_duration', type=int, help='moving average window duration in seconds', default=300)

    args = parser.parse_args()

    log_file_list = glob.glob(os.path.join(args.log_folder, '*.log'))

    log_file = None

    for file in log_file_list:
        if args.id in file:
            log_file = file

    if log_file == None:
        for file in log_file_list:
            print('[ {} ]'.format(file))
        print('[ ID {} not found ]'.format(args.id))
        return

    chat_history = load_chat(log_file)

    chat_time_list = [getattr(chat, 'time') for chat in chat_history]

    time_range_string_list = plot_chat_time_histogram(chat_time_list, args.segment_duration, args.mov_avg_duration, args.sigma)

    file_name = '{}={}.txt'.format(args.id, datetime.now().strftime("%H-%M-%S"))

    result_file_path = os.path.join(args.output_folder, file_name)

    with open(result_file_path, 'w') as file:
        for arg in vars(args):
            print(arg, getattr(args, arg), file=file)

        print('', file=file)

        for time_range in time_range_string_list:
            print(time_range, file=file)

if __name__ == '__main__':
    main()
