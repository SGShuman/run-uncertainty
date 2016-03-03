import numpy as np
import matplotlib.pyplot as plt

def time_in_sec(lst):
    '''Return a list of seconds from a list of time in mm:ss format'''
    output = []
    for time in lst:
        time_lst = time.split(':')
        if len(time_lst) == 3:
            [hours, mins, secs] = time_lst
        else:
            [mins, secs] = time_lst
        output.append(int(mins)*60 + int(secs))
    return np.array(output)

def time_in_min(secs):
    '''Return a formatted time string from a secs int'''
    hours = int(secs / 3600)
    mins = int(secs / 60) - hours * 60
    secs = int(secs % 60)
    if secs < 10:
        secs = '0' + str(secs)
    if mins < 10:
        mins = '0' + str(mins)
    if hours:
        return '%s:%s:%s' % (hours, mins, secs)
    else:
        return '%s:%s' % (mins, secs)

def calc_unc(times1, times2):
    '''Return the main time, pace and uncertainty calculations'''
    tot_time = (np.sum(times1) + np.sum(times2)) / 2.
    unc = np.abs(times1 - times2)
    tot_unc = np.sqrt(np.sum(unc ** 2))
    pace = np.mean(times1)
    pace = time_in_min(pace)
    pace_unc = tot_unc / np.sqrt(len(times1))
    return tot_time, np.around(tot_unc, 2), pace, np.around(pace_unc, 2)

def calc_95_ci(time, unc):
    '''Return a tuple of (95_ci_high, 95_ci_low)'''
    [secs] = time_in_sec([time])
    high = secs + 1.96 * unc
    low = secs - 1.96 * unc
    return (time_in_min(high), time_in_min(low))

if __name__ == '__main__':
    # j_times is Strava data (ran by Joel)
    j_times = ['7:47', '8:06', '7:47', '8:01', '7:57', '7:59', '7:58', '8:20', '8:22', '8:27']
    # s_times is Nike data (ran by Scott)
    s_times = ['7:55', '8:06', '7:41', '7:56', '7:57', '8:04', '7:55', '8:19', '8:27', '8:29']
    miles = np.arange(10)

    # Do Calculations
    j_secs = time_in_sec(j_times)
    s_secs = time_in_sec(s_times)
    tot_time, tot_unc, pace, pace_unc = calc_unc(j_secs, s_secs)
    print "Total Time: %s, Time Uncertainty: %s, Pace: %s, Pace Uncertainty: %s" % (
    time_in_min(tot_time), tot_unc, pace, pace_unc
    )
    print calc_95_ci(pace, pace_unc)

    # Graph it!
    width = .35
    x = np.append(miles, 10)
    yerr = np.append(np.abs(j_secs - s_secs), pace_unc)
    height_strava = np.append(j_secs, np.mean(j_secs))
    height_nike = np.append(s_secs, np.mean(s_secs))
    plt.bar(x, height_strava, width, yerr=yerr, alpha=.35, label='Strava')
    plt.bar(x+width, height_nike, width, yerr=yerr, alpha=.35, color='g', label='Nike')
    plt.legend(loc=2)
    plt.yticks(np.arange(0, 660, 60), np.arange(11))
    plt.xticks(np.arange(11) + width, list(np.arange(1, 11)) + ['Avg Pace'])
    plt.ylabel('Time in Minutes')
    plt.xlabel('Mile Number')
    plt.title('Mile Times w/ Uncertainty')
    plt.ylim((7*60, 9*60))
    plt.xlim((-width, 11))
    plt.show()
