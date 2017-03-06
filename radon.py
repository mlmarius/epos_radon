# -*- coding: utf-8 -*-
import handler
import tornado.ioloop
import tornado.web
import tornado.escape
from request_manager_radon import RequestManagerRadon
import mysql.connector
import json
from ConfigParser import ConfigParser
import os
import decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


class MainHandler(handler.APIBaseHandler):

    def initialize(self, config):
        self.config = config

    def get(self):
        manager = RequestManagerRadon()
        user_request = manager.bind(self).validate()
        if user_request.is_valid:
            args = user_request.getArgs()
            args['DIV'] = 1000000

            args['min_period'] = 60
            args['max_period'] = 180
            args['max_int_delta'] = 3600

            cnx = mysql.connector.connect(user=self.config.get('db', 'user'),
                                          password=self.config.get('db', 'pass'),
                                          database=self.config.get('db', 'db'),
                                          host=self.config.get('db', 'host'))

            cursor = cnx.cursor(dictionary=True)

            query = '''

CREATE TEMPORARY TABLE IF NOT EXISTS rn_table AS
(
select
(((a.value/d.samp_rate)-d.background)/d.efficiency) as radon_value,
      (sqrt(a.value)/a.value)*100 as radon_error,
      DATE_FORMAT(a.time_acq,'%Y-%m-%dT%H:%i:%s') as value_time,
      b.net as network_code,
      b.sta as station_code,
      b.loc as station_location,
      b.lat as station_latitude,
      b.lon as station_longitude,
      b.elevation as station_elevation,
      c.value as installation_type,
      e.value as temperature_in
from
geochemical1 a,
station b,
installation_type c,
sens_geochemical_params d,
sens_t_int e
where
a.fk_sens_geochemical_params=d.id and
a.fk_station = b.id and
b.id = e.fk_station and
(b.lat between {minlat} and {maxlat}) and
(b.lon between {minlon} and {maxlon}) and
(a.time_acq between '{mintime}' and '{maxtime}') and
abs(TIMESTAMPDIFF(microsecond,a.time_acq,e.time_acq)/{DIV}) < {max_int_delta} and
(d.samp_rate between {min_period} and {max_period}) and c.value like '{type_site}' having radon_error <= {max_radon_error}
);
select
radon_value,
radon_error,
value_time,
network_code,
station_code,
station_location,
station_latitude,
station_longitude,
station_elevation,
installation_type,
avg(temperature_in) as mean_temperature_in
from
rn_table
group by
network_code,
station_code,
station_location,
station_latitude,
station_longitude,
station_elevation,
installation_type,
value_time,
radon_value,
radon_error
            '''.format(**args)

            for result in cursor.execute(query, multi=True):
                if result.with_rows:
                    # print("Rows produced by statement '{}':".format(result.statement))
                    resp = self.render_string('response.json', result=json.dumps(result.fetchall(), cls=DecimalEncoder))
                    self.write(resp)
                    self.set_header('Content-Type', 'application/json')
                    return
                else:
                    # this is the temptable query response
                    pass
                    # print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))
            return

        else:
            errors = [e.message for e in user_request.global_errors] + [e.message for (p, e) in user_request.errors]
            return self.send_error_response(errors)


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        queries = []

        # add some example queries
        queries.append(dict(
            minlat=43.10,
            maxlat=43.80,
            minlon=12.10,
            maxlon=12.80,
            mintime='2010-03-01T00:00:00.000',
            maxtime='2011-05-01T00:00:00.000',
            # min_period='PT60S',
            # max_period='PT180S',
            min_period='60',
            max_period='180',
            type_site='indoor'
        ))

        for idx, q in enumerate(queries):
            queries[idx] = '&'.join(['{}={}'.format(k, v) for k, v in q.iteritems()])
        # transform the queries into http query strings
        queries = ['/query?%s' % q for q in queries]

        manager = RequestManagerRadon()

        self.render('index.html', queries=queries, manager=manager)

if __name__ == "__main__":

    defaults = dict(port=8888)

    cfg = ConfigParser(defaults)
    cfg.read('config.ini')

    # if environment configuration is present then override whatever there is
    # usefull for overriding configuration in Docker mode
    # environment variables should look like this EP_SECTIONNAME_VARNAME_HERE='value'
    env_config = {key[3:].lower(): val for key, val in os.environ.items() if key.startswith('EP_')}
    for k, v in env_config.items():
        keyparts = k.split('_')
        sectionname = keyparts[0]
        varname = '_'.join(keyparts[1:])
        cfg.set(sectionname, varname, v)

    settings = dict(
        debug=True,
        template_path='templates/'
    )

    application = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/query", MainHandler, dict(config=cfg))
    ], **settings)
    application.listen(cfg.get('service', 'port'))
    tornado.ioloop.IOLoop.current().start()
