#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import time
import multiprocessing
import sys
import argparse


def _loop(throttle=100):
    sleep_duration = (100 - throttle) / 1000
    process_bedtime = time.time() + 0.1 - sleep_duration
    while True:
        now = time.time()
        if now < process_bedtime:
            continue
        time.sleep(sleep_duration)
        process_bedtime = time.time() + 0.1 - sleep_duration


def _execute(args):
    processes = []
    for _ in range(args.cores):
        process = multiprocessing.Process(
            target=_loop,
            args=(args.throttle,),
        )
        process.daemon = True
        process.start()
        processes.append(process)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        return 0
    except:
        return 1
    finally:
        for process in processes:
            process.terminate()


def _validate(args):
    system_cpu_cores = multiprocessing.cpu_count()

    if args.cores < 1:
        fmt = 'warning: argument -c/--cores:'
        'specify value the system actually does have: (1 ~ {cores})'
        msg = fmt.format(
            cores=system_cpu_cores,
        )
        print(msg, file=sys.stderr)
        args.cores = 1

    if args.cores > system_cpu_cores:
        fmt = 'warning: argument -c/--cores:'
        'specify value the system actually does have: (1 ~ {cores})'
        msg = fmt.format(
            cores=system_cpu_cores,
        )
        print(msg, file=sys.stderr)
        args.cores = system_cpu_cores

    if args.throttle < 1:
        msg = 'warning: argument -t/--throttle:'
        'specify value between 1 to 100'
        print(msg, file=sys.stderr)
        args.args.throttle = 1

    if args.throttle > 100:
        msg = 'warning: argument -t/--throttle:'
        'specify value between 1 to 100'
        print(msg, file=sys.stderr)
        args.args.throttle = 100


def _parse_args():
    description = 'Warm your computer'
    arg_parser = argparse.ArgumentParser(description=description)

    option_c_help = 'CPU core numbers'
    default_cores = multiprocessing.cpu_count()
    arg_parser.add_argument(
        '-c', '--cores',
        type=int,
        required=False,
        default=default_cores,
        help=option_c_help,
    )

    option_t_help = 'CPU throttle (%%)'
    default_throttle = 100
    arg_parser.add_argument(
        '-t', '--throttle',
        type=int,
        required=False,
        default=default_throttle,
        help=option_t_help,
    )

    return arg_parser.parse_args()


def main():
    args = _parse_args()
    _validate(args)
    exit_code = _execute(args)
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
