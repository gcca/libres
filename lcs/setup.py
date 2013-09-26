# -*- coding: utf-8 -*-

import sys
import os
from codecs import open
from base64 import b64decode
import argparse
import lsc
import lessc

def depender(dependencias, dir):
    dep_cod = ''

    if dependencias:
        map_sufijo_dep = {
            '.js'  : '-min.js',
            '.css' : '.css'
        }

        sufijo_dep = map_sufijo_dep[sufijo]

        for dep in dependencias:
            dep_f = os.path.join(dir, dep + sufijo_dep)

            with open(dep_f, 'r', 'utf-8') as f_dep:
                dep_cod += f_dep.read()

    return dep_cod

parser = argparse.ArgumentParser(description='''
Compilador del proyecto
''')

parser.add_argument('fichero')
parser.add_argument('--salida', dest='salida')
parser.add_argument('-s'      , dest='salida')

parser.add_argument('--sufijo')

parser.add_argument('-O', action='store_true', dest='optimizar')

parser.add_argument('--externas')

parser.add_argument('--internas')

parser.add_argument('--compresor_js')
parser.add_argument('--compresor_css')

parser.add_argument('--3rdparty', dest='dir_dependencias')

class AccionDepurar(argparse.Action):
    def __call__(self, parser, contexto, vals, option_string=None):
        setattr(contexto, self.dest, '1' if vals is None else vals)

parser.add_argument('--depurar', nargs='?', action=AccionDepurar)

args = parser.parse_args()

fichero         = args.fichero
sufijo         = args.sufijo
salida         = args.salida
dir_dependencias = args.dir_dependencias

if args.externas: args.externas = args.externas.split(',')
if args.internas: args.internas = args.internas.split(',')

if not sufijo:
    f_suf = os.path.splitext(fichero)[1]

    map_s = {
        '.ls'    : '.js',
        '.less' : '.css'
    }

    sufijo = map_s[f_suf]


# (-o-) decidir cómo compilar
map_compilador = {
    '.js'  : lsc.compilar,
    '.css' : lessc.compilar
}

compilar = map_compilador[sufijo]

try:
    compilado = compilar(args.fichero)
except Exception as ex:
    print(ex)
    sys.exit(-1)


if not salida:
    print(compilado)
else:
    f_nom      = os.path.basename(fichero)
    f_nombase = os.path.splitext(f_nom)[0]

    salida_f = os.path.join(salida, f_nombase) + sufijo

    tmp_b = '/dev/shm' if 'posix' == os.name \
        else os.path.join(os.path.dirname(__file__), 'base')

    salida_tmp_f  = os.path.join(tmp_b, f_nombase) + sufijo

    map_nom = os.path.join(tmp_b, 'mapr-' + f_nombase )
    if '.js' == sufijo and not os.path.exists(map_nom):
        print('Error: Compilar antes el *.less')
        sys.exit(0)

    if args.optimizar:
        # -------------------------------------
        # map_compresor = {
        #     '.js' : 'java -jar %(compresor)s --language_in ECMASCRIPT5_STRICT --compilation_level %(nivel)s --process_closure_primitives --js %(mapa)s --js %(entrada)s --js_output_file %(salida)s',

        #     '.css' : 'java -jar %(compresor)s --output-file %(salida)s --output-renaming-map-format CLOSURE_COMPILED --rename %(nivel)s --output-renaming-map %(mapa)s --allow-unrecognized-functions --allow-unrecognized-properties %(entrada)s'
        # }

        map_compresor =  {
           '.js' : b64decode('amF2YSAtamFyICUoY29tcHJlc29yKXMgLS1sYW5ndWFnZV9pbiBFQ01BU0NSSVBUNV9TVFJJQ1QgLS1jb21waWxhdGlvbl9sZXZlbCAlKG5pdmVsKXMgLS1wcm9jZXNzX2Nsb3N1cmVfcHJpbWl0aXZlcyAtLWpzICUobWFwYSlzIC0tanMgJShlbnRyYWRhKXMgLS1qc19vdXRwdXRfZmlsZSAlKHNhbGlkYSlz'),

           '.css' : b64decode('amF2YSAtamFyICUoY29tcHJlc29yKXMgLS1vdXRwdXQtZmlsZSAlKHNhbGlkYSlzIC0tb3V0cHV0LXJlbmFtaW5nLW1hcC1mb3JtYXQgQ0xPU1VSRV9DT01QSUxFRCAtLXJlbmFtZSAlKG5pdmVsKXMgLS1vdXRwdXQtcmVuYW1pbmctbWFwICUobWFwYSlzIC0tYWxsb3ctdW5yZWNvZ25pemVkLWZ1bmN0aW9ucyAtLWFsbG93LXVucmVjb2duaXplZC1wcm9wZXJ0aWVzICUoZW50cmFkYSlz')
        }

        #if args.depurar:
            #map_nivel_compresor = {
                ## '.js'  : 'WHITESPACE_ONLY --formatting PRETTY_PRINT --debug',
                #'.js'    : b64decode('V0hJVEVTUEFDRV9PTkxZIC0tZm9ybWF0dGluZyBQUkVUVFlfUFJJTlQgLS1kZWJ1Zw=='),
                ##'.css' : 'DEBUG --pretty-print'
                #'.css' : b64decode('REVCVUcgLS1wcmV0dHktcHJpbnQ=')
            #}
        #else:
        map_nivel_compresor = {
            #'.js'    : 'ADVANCED_OPTIMIZATIONS',
            '.js'  : b64decode('QURWQU5DRURfT1BUSU1JWkFUSU9OUw=='),
            #'.css' : 'CLOSURE'
            '.css' : b64decode('Q0xPU1VSRQ==')
        }

        map_ruta_compresor = {
            '.js'  : args.compresor_js,
            '.css' : args.compresor_css
        }

        compresor       = map_compresor       [sufijo]
        nivel_compresor = map_nivel_compresor [sufijo]
        ruta_compresor  = map_ruta_compresor  [sufijo]
        # -------------------------------------

        entrada_tmp_f = os.path.join(tmp_b, f_nom)

        with open(entrada_tmp_f, 'w', 'utf-8') as f_entrada:
            int_cod = depender(args.internas, dir_dependencias)
            # getCssName
            renam = b64decode('Z29vZy5nZXRDc3NOYW1l')
            # Css
            renom = b64decode('Z3ouQ3Nz')
            f_entrada.write(int_cod + compilado.replace(renom, renam))

        if '.js' == sufijo:
            if args.depurar:
                # '--formatting PRETTY_PRINT'
                depurar = ' ' + b64decode('LS1mb3JtYXR0aW5nIFBSRVRUWV9QUklOVA==')
                if '2' == args.depurar:
                    # '--debug'
                    #depurar += ' ' + b64decode('LS1kZWJ1Zw==')
                    # 'SIMPLE_OPTIMIZATIONS'
                    nivel_compresor = b64decode('U0lNUExFX09QVElNSVpBVElPTlM=')

                compresor += depurar

            if args.externas:
                for ext in args.externas:
                    compresor += ' --externs %s' % os.path.join(dir_dependencias,
                                                                ext + sufijo)

        os.system(compresor % {
            'compresor' : ruta_compresor,
            'entrada'   : entrada_tmp_f,
            'salida'    : salida_tmp_f,
            'mapa'      : map_nom,
            'nivel'     : nivel_compresor
        })

        if '.css' == sufijo:
            map_s = ''
            with open(map_nom, 'r') as map_f:
                map_s = map_f.read().replace(' ', '').replace('\n', '')
            with open(map_nom, 'w') as map_f:
                map_f.write(map_s)

        os.remove(entrada_tmp_f)

        #with open(salida_tmp_f, 'r', 'utf-8') as f_salida_tmp:
            #salida_limpia = f_salida_tmp.read().replace('\n', ' ')

        #with open(salida_tmp_f, 'w', 'utf-8') as f_salida_tmp:
            #f_salida_tmp.write(salida_limpia)

    else:
        if '.js' == sufijo:
            if not args.externas:
                #args.externas.append('base')
                args.externas = []
            args.externas.append(b64decode('YmFzZQ=='))
            with open(salida_tmp_f, 'w') as f_sal:
                int_cod = depender(args.internas, dir_dependencias)

                #with open('renaming_map.js', 'r') as f_rem:
                #with open(b64decode('cmVuYW1pbmdfbWFwLmpz'), 'r') as f_rem:
                with open(map_nom, 'r') as f_rem:
                    f_sal.write(f_rem.read() \
                                    .replace(' ', '') \
                                    .replace('\n', '')
                                + int_cod.encode('utf-8') + compilado \
                                    #.replace('gz.Css', 'gzc.Css') \
                                    #.replace(b64decode('Z3ouQ3Nz'), b64decode('Z3pjLkNzcw==')) \
                                    .encode('utf-8'))
        elif '.css' == sufijo:
            entrada_tmp_f = os.path.join(tmp_b, f_nom)

            with open(entrada_tmp_f, 'w', 'utf-8') as f_entrada:
                int_cod = depender(args.internas, dir_dependencias)
                # getCssName
                renam = b64decode('Z29vZy5nZXRDc3NOYW1l')
                # Css
                renom = b64decode('Z3ouQ3Nz')
                f_entrada.write(int_cod + compilado.replace(renom, renam))

            compresor = b64decode('amF2YSAtamFyICUoY29tcHJlc29yKXMgLS1vdXRwdXQtZmlsZSAlKHNhbGlkYSlzIC0tb3V0cHV0LXJlbmFtaW5nLW1hcC1mb3JtYXQgQ0xPU1VSRV9DT01QSUxFRCAtLXJlbmFtZSAlKG5pdmVsKXMgLS1vdXRwdXQtcmVuYW1pbmctbWFwICUobWFwYSlzIC0tYWxsb3ctdW5yZWNvZ25pemVkLWZ1bmN0aW9ucyAtLWFsbG93LXVucmVjb2duaXplZC1wcm9wZXJ0aWVzICUoZW50cmFkYSlz')
            os.system(compresor % {
                'compresor' : args.compresor_css,
                'entrada'   : entrada_tmp_f,
                'salida'    : salida_tmp_f,
                'mapa'      : map_nom,
                'nivel'     : 'DEBUG'
            })

            os.remove(entrada_tmp_f)
            sys.exit(0)

            # with open(salida_tmp_f, 'w') as f_sal:
            #     f_sal.write(compilado.encode('utf-8'))

            #os.rename(entrada_tmp_f, )


            # with open(map_nom, 'w') as map_f:
            #     #map_f.write('goog.setCssNameMapping({});')
            #     map_f.write(b64decode('Z29vZy5zZXRDc3NOYW1lTWFwcGluZyh7fSk7'))
            #     int_cod = depender(args.internas, dir_dependencias)
            #     compilado = int_cod + compilado


        args.depurar = '1'

    ext_cod = depender(args.externas, dir_dependencias) if args.externas else ''

    derechos = b64decode('LyoqCiAqIENhdmFTb2Z0IFNBQyBodHRwOi8vY2F2YXNvZnRzYWMuY29tCiAqIGNyaXN0SGlhbiBHei4gKGdjY2EpIC0gaHR0cDovL2djY2EudGsKICovCg==')

    with open(salida_f, 'w', 'utf-8') as f_salida:
        with open(salida_tmp_f, 'r', 'utf-8') as f_salida_tmp:
            salida = f_salida_tmp.read()
            compilado = (ext_cod.replace('\n', ' ') + salida) \
                if args.depurar \
                else (ext_cod + salida).replace('\n', ' ')
            f_salida.write(derechos + compilado)

    os.remove(salida_tmp_f)
