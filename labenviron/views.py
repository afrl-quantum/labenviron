import datetime, StringIO
import numpy as np

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.urlresolvers import reverse

from labenviron import models

import plotter

# Create your views here.

def index(request):
  jquery = static('labenviron/js/jquery-3.2.1.min.js')
  reload_interval = 300
  data_url = reverse('data')
  plot_url = reverse('plot')

  page = """\
  <html>
  <header>
    <title>Lab Environmental Data Viewer</title>
    <script src="{jquery}"></script>
    <script>
      function get_timeout() {{
        // input is in seconds
        v = $('input[name=interval]')[0].value;
        if (v == '') {{
          v = {reload_interval};
        }}
        return v * 1000;
      }}

      function change_download() {{
        var link = $('#download_data');
        link.attr('href', '{data_url}'
                  + '?host=' + $('#host').val()
                  + '&date_begin='  + $('#date_begin').val()
                  + '&date_end='    + $('#date_end').val()
                  );
        return true;
      }}

      function do_reload() {{
        //location.reload();
        var D = $('#plot');
        var H = $('#host').val();
        var D0 = $('#date_begin').val();
        var D1 = $('#date_end').val();
        var T0 = $('#temp_lo').val();
        var T1 = $('#temp_hi').val();
        var P0 = $('#press_lo').val();
        var P1 = $('#press_hi').val();
        var H0 = $('#humid_lo').val();
        var H1 = $('#humid_hi').val();
        var P = $('.ui-page');
        var I = $('input[name=interval]');
        console.log('I.width: ' + I.width());
        pixel_sz = 1.96/I.width();
        console.log('pixel_sz: ' + pixel_sz);
        console.log('P.width: ', P.width());
        console.log('P.height: ', P.height());
        var vertical_save = 5*(pixel_sz * I.height());
        var width   = pixel_sz*P.width() * 0.95;
        var height  = 4.5;//pixel_sz*P.height() - vertical_save;

        // clear this in case we are requested 'now'
        clearTimeout( window.reload_timer );
        console.log('requesting plot of size: ' + width + ',' + height);
        $.ajax({{
          type : 'GET',
          url  : '{plot_url}',
          data : {{
            host        : H,
            date_begin  : D0,
            date_end    : D1,
            temp_lo     : T0,
            temp_hi     : T1,
            press_lo    : P0,
            press_hi    : P1,
            humid_lo    : H0,
            humid_hi    : H1,
            width       : width,
            height      : height
          }},
          dataType : 'html'
        }})
        .done( function( data ) {{
          D = $('#plot');
          D.children().remove(); // delete all old children
          D.append( data );
        }})
        .fail( function() {{
          console.log('Could not download updated environment plot');
        }})
        .always( function() {{
          reset_timer();
        }});

        change_download();
      }}

      /* Time at which reload should occur */
      var next_reload_at = 0;

      function reset_timer() {{
        console.log('scheduling next plot refresh...');
        clearTimeout( window.reload_timer );
        var dt = get_timeout();
        next_reload_at = Date.now() + dt;
        window.reload_timer = setTimeout( do_reload, dt );
      }}

      function show_reload_time() {{
        var t = (next_reload_at - Date.now()) / 1000.0 | 0
        $('#next_reload').text(t + ' s');
      }}

      /* start the update happening at all times. */
      $(document).ready( function() {{
        do_reload(); // first time for everything
        setInterval(show_reload_time, 1000);

        $('input[name=interval]').change( function() {{ reset_timer(); }});
        $('#plot_data').on('click', function (e){{ do_reload(); }});
        $('#download_data').on('click', function (e){{ return change_download(); }});
      }});
    </script>
  </header>
  <body>
    <center>
      <h1>Laboratory Environmental Viewer</h1>
    </center>
    <form action='javascript:void(0);' id='plot_form'>
    <hr>
      <div style='width: 100%;text-align:center;' id='plot'>  </div>
    <hr>
      <table align=center>
      <tr>
        <td>
          Host:
          <select id=host>
            {host_options}
          </select>
        </td>
        <td>Date Range:</td><td>
          <input type=date id='date_begin'/> <b>:</b>
          <input type=date id='date_end'/>
        </td>
      </tr>
      <tr>
        <td/>
        <td>Temperature Scale:</td><td>
          <input type=number id='temp_lo'/> <b>:</b>
          <input type=number id='temp_hi'/> C
        </td>
      </tr>
      <tr>
        <td/>
        <td>Pressure Scale:</td><td>
          <input type=number id='press_lo'/> <b>:</b>
          <input type=number id='press_hi'/> hPa
        </td>
      </tr>
      <tr>
        <td/>
        <td>Humidity Scale:</td><td>
          <input type=number id='humid_lo'/> <b>:</b>
          <input type=number id='humid_hi'/> %
        </td>
      </tr>
      <tr>
        <td colspan=2>
          <input type=number placeholder='Reload Interval [{reload_interval} s]'
           name='interval' min=1/><br>
          Next reload at: <div style='display:inline;' id='next_reload'></div>
        </td>
        <td colspan=2 align=center>
        <input type=button id=plot_data value="Re-Plot Data"/>
        <a id='download_data' href="#" download="environmental-data.txt">Download</a>
        </td>
      </table>
    </form>
  </body>
  </html>
  """
  host_options = [
    '<option>{}</option>'.format(h)
    for (h,) in models.LabData.objects.order_by('host').values_list('host').distinct()
  ]

  return HttpResponse( page.format(**locals()) )


def data(request):
  kw = dict()
  kw['host'] = request.GET.get('host',  None) #defaults to today
  kw['D0'] = request.GET.get('date_begin',  None) #defaults to today
  kw['D1'] = request.GET.get('date_end',    None) #defaults to today
  data = plotter.get_data(**kw)
  output = StringIO.StringIO()
  output.write(
    '# Environmental Lab Data\n'
    '# Host: {host}\n'
    '# Date range: {D0} -- {D1}\n'
    '# Columns:  {columns}\n'
    .format(columns=',\t'.join(models.LabData.array_order), **kw)
  )
  np.savetxt(output, data)
  return HttpResponse(output.getvalue(),  content_type='text/plain')


def plot(request):
  kw = dict()
  kw['host'] = request.GET.get('host',  None) #defaults to today
  kw['D0'] = request.GET.get('date_begin',  None) #defaults to today
  kw['D1'] = request.GET.get('date_end',    None) #defaults to today
  kw['T0'] = request.GET.get('temp_lo',  None)
  kw['T1'] = request.GET.get('temp_hi',  None)
  kw['P0'] = request.GET.get('press_lo', None)
  kw['P1'] = request.GET.get('press_hi', None)
  kw['H0'] = request.GET.get('humid_lo', None)
  kw['H1'] = request.GET.get('humid_hi', None)
  return HttpResponse(plotter.get_sensor_plot(**kw))
