# -*- coding: utf-8 -*-
from requestutils.request import Request
from requestutils.request_param import RequestParam
import requestutils.validators as v


class RequestManagerRadon(object):

    def __init__(self):

        def dateFormatter(dtobj):
            return dtobj.isoformat()

        rq = Request()
        mintime = RequestParam('mintime',
                     name="UTC minimum date and time",
                     description='''UTC minimum date and time
                     meaning: data are extracted if related time is greater equal to mintime
                     standard reference:  ISO 8601 (YYYY-MM-DDThh:mm:ss.ccc)''',
                     validators=[v.ValidatorDateTimeRange('1970-01-01T00:00:00.000', 'now')]
                     )
        mintime.setOutputFormatter(dateFormatter)
        mintime.addTo(rq)

        maxtime = RequestParam('maxtime',
                     name="UTC maximum date and time",
                     description='''UTC maximum date and time
                     meaning: data are extracted if related time is less or equal to maxtime
                     standard reference:  ISO 8601 (YYYY-MM-DDThh:mm:ss.ccc)''',
                     validators=[v.ValidatorDateTimeRange('1970-01-01T00:00:00.000', 'now')]
                     )
        maxtime.setOutputFormatter(dateFormatter)
        maxtime.addTo(rq)

        # ensure mintime is smaller than maxtime
        # rq.addPostValidator(v.ValidatorPostSmaller('mintime', 'maxtime'))

        #
        # Geographic region parameters
        #

        RequestParam('minlat',
                     name='Minimum latitude of the selection area',
                     description='''earthquakes and stations to calculate Vp/Vs are extracted if latitude is greater or equal to minlat
                     standard reference:  ISO 6709''',
                     validators=[v.ValidatorNumberRange(-90, 90)]
                     ).addTo(rq)

        RequestParam('maxlat',
                     name='Maximum latitude of the selection area',
                     description='''earthquakes and stations to calculate Vp/Vs are extracted if latitude is less or equal to maxlat
                     standard reference:  ISO 6709''',
                     validators=[v.ValidatorNumberRange(-90, 90)]
                     ).addTo(rq)

        rq.addPostValidator(v.ValidatorPostSmaller('minlat', 'maxlat'))

        RequestParam('minlon',
                     name='Minimum longitude of the selection area',
                     description='''earthquakes and stations to calculate Vp/Vs are extracted if longitude is greater or equal to minlon
                     standard reference:  ISO 6709''',
                     validators=[v.ValidatorNumberRange(-180, 180)]
                     ).addTo(rq)

        RequestParam('maxlon',
                     name='Maximum longitude of the selection area',
                     description='''earthquakes and stations to calculate Vp/Vs are extracted if longitude is less or equal to maxlon
                     standard reference:  ISO 6709''',
                     validators=[v.ValidatorNumberRange(-180, 180)]
                     ).addTo(rq)

        rq.addPostValidator(v.ValidatorPostSmaller('minlon', 'maxlon'))

        RequestParam('min_period',
                     unit='period, according to the standard',
                     name='minimum "sampling period" allowed to extract data',
                     description='''the period is a setup of each station and defines the time interval between one measure and another
                     standard reference:  ISO 8601 (P[n]Y[n]M[n]DT[n]H[n]M[n]S)
                     ''',
                     default='PT60M',
                     validators=[v.ValidatorRegex(r"^P(?!$)(\d+Y)?(\d+M)?(\d+W)?(\d+D)?(T(?=\d+[HMS])(\d+H)?(\d+M)?(\d+S)?)?$")]
                     ).addTo(rq)

        RequestParam('max_period',
                     unit='period, according to the standard',
                     name='maximum "sampling period" allowed to extract data',
                     description='''the period is a setup of each station and defines the time interval between one measure and another
                     standard reference:  ISO 8601 (P[n]Y[n]M[n]DT[n]H[n]M[n]S)
                     ''',
                     default='PT1D',
                     validators=[v.ValidatorRegex(r"^P(?!$)(\d+Y)?(\d+M)?(\d+W)?(\d+D)?(T(?=\d+[HMS])(\d+H)?(\d+M)?(\d+S)?)?$")]
                     ).addTo(rq)

        RequestParam('type_site',
                     default='all',
                     name='maximum "sampling period" allowed to extract data',
                     description='''it is a description (varchar) of the type of installation of the sensor at the site, (indoor, shelter, borehole, soil)''',
                     validators=[v.ValidatorRegex('^all|indoor|shelter|borehole|soil$')]
                     ).addTo(rq)


        RequestParam('max_radon_error',
                     default=51,
                     name='maximum % uncertainty of the measure accepted for extraction',
                     description='(sqrt(counts)/counts)*100',
                     validators=[v.ValidatorNumberRange(0,100)]
                     ).addTo(rq)

        RequestParam('max_int_delta',
                     unit='period, according to the standard',
                     default='PT3600S',
                     name='maximum distance in time between internal temperature measure timing and correspondent Rn measure time',
                     description='''internal temperature timing can be different from that of Rn, so temperature measure are referred to Rn measure if time distance is <=  max_int_delta; mean temperature value is given as input referred to the Rn measure
                     standard reference:   ISO 8601 (P[n]Y[n]M[n]DT[n]H[n]M[n]S)''',
                     validators=[v.ValidatorRegex(r"^P(?!$)(\d+Y)?(\d+M)?(\d+W)?(\d+D)?(T(?=\d+[HMS])(\d+H)?(\d+M)?(\d+S)?)?$")]
                     ).addTo(rq)

        self.rq = rq

    def bind(self, userargs):
        self.rq.bind(userargs)
        return self

    def validate(self):
        self.rq.validate()
        return self.rq
