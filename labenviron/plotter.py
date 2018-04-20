#!/usr/bin/env python3
# vim: et:ts=2:sw=2:tw=80:nowrap

# our current global for storing link to alarm client
import matplotlib
if __name__ != '__main__':
  matplotlib.use('Agg')
else:
  import sys, os
  THIS_DIR = os.path.dirname(__file__)
  sys.path.insert(0, os.path.join(THIS_DIR, os.path.pardir))
  import sensors.outside


font = {
#  'family' : 'monospace',
#  'weight' : 'extrabold',
    'size'   : 8,
}
matplotlib.rc('font', **font)


import matplotlib.pyplot as plt
from matplotlib.colors import ColorConverter
import numpy as np
import mpld3
import datetime, time
from labenviron.models import LabData


def get_data(host, D0, D1):
  if D0 is None or D0 == '':
    D0 = datetime.date.today()
  else:
    D0 = datetime.datetime.strptime(D0, '%Y-%m-%d')
  if D1 is None or D1 == '':
    D1 = datetime.date.today()
  else:
    D1 = datetime.datetime.strptime(D1, '%Y-%m-%d')

  D0 = datetime.datetime.combine(D0, datetime.time.min)
  D1 = datetime.datetime.combine(D1, datetime.time.max)

  # get the data (Gregorian ordinal(date), temperature, pressure, humidity)
  query = LabData.objects.filter(time__range=(D0,D1))
  if host:
    query = query.filter(host=host)

  return np.array([np.array(r) for r in query])


def mk_plot(host=None,
            D0=None, D1=None,
            T0=None, T1=None,
            P0=None, P1=None,
            H0=None, H1=None,
            width=8, height=5):

  data = get_data(host, D0, D1)

  fig, ax = plt.subplots(figsize=(width,height))
  fig.subplots_adjust(left=0.19, right=0.98, top=0.98)

  fix_ranges = ''
  # now we creat plot items for each event list
  if len(data) > 0:
    mnT = data[:,1].min()
    mxT = data[:,1].max()
    mnP = data[:,2].min()
    mxP = data[:,2].max()
    mnH = data[:,3].min()
    mxH = data[:,3].max()

    if T0 is None or T0 == '':
      T0 = mnT
    if T1 is None or T1 == '':
      T1 = mxT
    if P0 is None or P0 == '':
      P0 = mnP
    if P1 is None or P1 == '':
      P1 = mxP
    if H0 is None or H0 == '':
      H0 = mnH
    if H1 is None or H1 == '':
      H1 = mxH

    T0 = float(T0)
    T1 = float(T1)
    P0 = float(P0)
    P1 = float(P1)
    H0 = float(H0)
    H1 = float(H1)

    ax.plot_date( data[:,0], (data[:,1] - T0)/float(T1-T0), 'o-', label='T' )
    ax.plot_date( data[:,0], (data[:,2] - P0)/float(P1-P0), 'o-', label='P' )
    ax.plot_date( data[:,0], (data[:,3] - H0)/float(H1-H0), 'o-', label='H' )

    fix_ranges = """
    <script>
    $('#temp_lo').attr('placeholder', '{mnT}');
    $('#temp_hi').attr('placeholder', '{mxT}');
    $('#press_lo').attr('placeholder', '{mnP}');
    $('#press_hi').attr('placeholder', '{mxP}');
    $('#humid_lo').attr('placeholder', '{mnH}');
    $('#humid_hi').attr('placeholder', '{mxH}');
    </script>
    """.format(**locals())

  ax.set_xlabel('Date/Time')
  ax.grid(True)
  ax.legend(loc='best')
  return fix_ranges, fig, ax

def get_sensor_plot(*a, **kw):
  html, fig, ax = mk_plot(*a, **kw)
  try:
    return html + mpld3.fig_to_html( fig )
  finally:
    plt.close(fig)
    del fig, ax



if __name__ == '__main__':
  if False:
    print(get_sensor_plot())
  else:
    mk_plot()
    #mpld3.show()
    plt.show()
