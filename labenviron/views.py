from django.shortcuts import render
from django.http import HttpResponse

from labenviron import models

# Create your views here.

def index(request):
  page = """\
  Hello! Here is some data to show...<br>
  <a href="all">Data from all days</a><br>
  <hr>
  {day_links}
  """
  L = models.LabData.objects.all()

  dates = list( set([ i.time.date() for i in L ]) )
  dates.sort()

  lines = list()
  for d in dates:
    lines.append( '<a href="day/{date}">{date}</a>'.format(date=d.strftime('%Y%m%d')) )

  return HttpResponse( page.format( day_links='<br>'.join(lines)) )


def day(request, day):
  L = models.LabData.objects.filter(time__year=day[:4],
                                    time__month=day[4:6],
                                    time__day=day[6:8])

  lines = [ str(i) for i in L ]
  # these three lines are exactly the same as the previous line
  # lines = list()
  # for i in L:
  #   lines.append(str(i))

  return HttpResponse('Hello! Here is some data to show...<br>'+ '<br>'.join(lines))

def all(request):
  L = models.LabData.objects.all()

  lines = [ str(i) for i in L ]
  # these three lines are exactly the same as the previous line
  # lines = list()
  # for i in L:
  #   lines.append(str(i))

  return HttpResponse('Hello! Here is some data to show...<br>'+ '<br>'.join(lines))
