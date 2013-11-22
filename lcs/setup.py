# -*- coding: utf-8 -*-

import sys
import os
from codecs import open
from base64 import b64decode as bde
import argparse
import lsc
import lessc
import jadec

def depender(dependencias, dir_):
    dep_cod = ''

    if dependencias:
        map_sufijo_dep = {
            '.js'  : '-min.js',
            '.css' : '.css'
        }

        sufijo_dep = map_sufijo_dep[sufijo]
        sufijo_rea = sufijo_dep

        for dep in dependencias:
            sufijo_dep = sufijo_rea
            if '.js' == sufijo and not args.optimizar and os.path.exists(os.path.join(dir_, dep + '-all.js')):
                sufijo_dep = '-all.js'

            dep_f = os.path.join(dir_, dep + sufijo_dep)

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
    if '.js' == sufijo:
        runtime = r'''var jade=jade||{};Array.isArray||(Array.isArray=function(b){return"[object Array]"==Object.prototype.toString.call(b)});Object.keys||(Object.keys=function(b){var a=[],c;for(c in b)b.hasOwnProperty(c)&&a.push(c);return a});jade.merge=function(b,a){var c=b["class"],d=a["class"];if(c||d)c=c||[],d=d||[],Array.isArray(c)||(c=[c]),Array.isArray(d)||(d=[d]),b["class"]=c.concat(d).filter(nulls);for(var e in a)"class"!=e&&(b[e]=a[e]);return b};function nulls(b){return null!=b&&""!==b} function joinClasses(b){return Array.isArray(b)?b.map(joinClasses).filter(nulls).join(" "):b}jade.cls=function(b,a){for(var c=[],d=0;d<b.length;d++)a&&a[d]?c.push(jade.escape(joinClasses([b[d]]))):c.push(joinClasses(b[d]));c=joinClasses(c);return c.length?' class="'+c+'"':""}; jade.attr=function(b,a,c,d){return"boolean"==typeof a||null==a?a?" "+(d?b:b+'="'+b+'"'):"":0==b.indexOf("data")&&"string"!=typeof a?" "+b+"='"+JSON.stringify(a).replace(/'/g,"&apos;")+"'":c?" "+b+'="'+jade.escape(a)+'"':" "+b+'="'+a+'"'};jade.attrs=function(b,a,c){var d=[],e=Object.keys(b);if(e.length)for(var h=0;h<e.length;++h){var f=e[h],g=b[f];if("class"==f){if(g=joinClasses(g))a&&a[f]?d.push(" "+f+'="'+jade.escape(g)+'"'):d.push(" "+f+'="'+g+'"')}else d.push(jade.attr(f,g,a&&a[f],c))}return d.join("")}; jade.escape=function(b){return String(b).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;")}; jade.rethrow=function rethrow(a,c,d,e){if(!(a instanceof Error))throw a;if(("undefined"!=typeof window||!c)&&!e)throw a.message+=" on line "+d,a;try{e=e||require("fs").readFileSync(c,"utf8")}catch(h){rethrow(a,null,d)}var f=3;e=e.split("\n");var g=Math.max(d-f,0),f=Math.min(e.length,d+f),f=e.slice(g,f).map(function(a,c){var e=c+g+1;return(e==d?"  > ":"    ")+e+"| "+a}).join("\n");a.path=c;a.message=(c||"Jade")+":"+d+"\n"+f+"\n\n"+a.message;throw a;}'''
        compilado = '%s\n%s\n%s' % (compilado[:12], runtime, compilado[12:])

        import re
        # jadeps = re.findall(r'([ ]*).*gzc.Jade\(\'(.*)\'\)', compilado)
        # jadeps = re.findall(r'gzc.Jade\(\'(.*)\'\)', compilado)
        jadeps = re.findall(bde('Z3pjLkphZGVcKFwnKC4qKVwnXCk='), compilado)

        repla = bde('Z3pjLkphZGUoJyVzJyk=')

        #for i, m in jadeps:
        for m in jadeps:
            lns = m.split('\\n')
            ln = lns[0]
            ns = len(ln[:-len(ln.lstrip())])
            js = jadec.ajade('\n'.join(l[ns:] for l in lns))
            cls = re.findall(r'class=\\"([a-zA-Z0-9- ]+)\\"', js)
            for cs in cls:
                js = js.replace(
                    r'class=\"%s\"' % cs,
                    'class=\\"" + %s + "\\"' % ' + " " + '.join(map(lambda x: 'gz.Css(\'%s\')' % x, cs.split())))
            js = re.sub(r' id=\\"([a-zA-Z0-9-]+)\\"', ' id=\\"" + gz.Css(\'\\1\') + "\\"', js)
            js = re.sub(r'{Css ([a-zA-Z0-9-]+)}', '" + gz.Css(\'\\1\') + "', js)
            # i = i + ' '
            # js = '\n'.join(i + l for l in js.split('\n'))
            # compilado = compilado.replace('gzc.Jade(\'%s\')' % m, js)
            compilado = compilado.replace(repla % m, js)

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
    if '.js' == sufijo and args.optimizar and not os.path.exists(map_nom):
        print('Error: Compilar antes el *.less')
        sys.exit(0)

    if args.optimizar:
        # -------------------------------------
        # map_compresor = {
        #     '.js' : 'java -jar %(compresor)s --language_in ECMASCRIPT5_STRICT --compilation_level %(nivel)s --process_closure_primitives --js %(mapa)s --js %(entrada)s --js_output_file %(salida)s',

        #     '.css' : 'java -jar %(compresor)s --output-file %(salida)s --output-renaming-map-format CLOSURE_COMPILED --rename %(nivel)s --output-renaming-map %(mapa)s --allow-unrecognized-functions --allow-unrecognized-properties %(entrada)s'
        # }

        map_compresor =  {
           '.js' : bde('amF2YSAtamFyICUoY29tcHJlc29yKXMgLS1sYW5ndWFnZV9pbiBFQ01BU0NSSVBUNV9TVFJJQ1QgLS1jb21waWxhdGlvbl9sZXZlbCAlKG5pdmVsKXMgLS1wcm9jZXNzX2Nsb3N1cmVfcHJpbWl0aXZlcyAtLWpzICUobWFwYSlzIC0tanMgJShlbnRyYWRhKXMgLS1qc19vdXRwdXRfZmlsZSAlKHNhbGlkYSlz'),

           '.css' : bde('amF2YSAtamFyICUoY29tcHJlc29yKXMgLS1vdXRwdXQtZmlsZSAlKHNhbGlkYSlzIC0tb3V0cHV0LXJlbmFtaW5nLW1hcC1mb3JtYXQgQ0xPU1VSRV9DT01QSUxFRCAtLXJlbmFtZSAlKG5pdmVsKXMgLS1vdXRwdXQtcmVuYW1pbmctbWFwICUobWFwYSlzIC0tYWxsb3ctdW5yZWNvZ25pemVkLWZ1bmN0aW9ucyAtLWFsbG93LXVucmVjb2duaXplZC1wcm9wZXJ0aWVzICUoZW50cmFkYSlz')
        }

        #if args.depurar:
            #map_nivel_compresor = {
                ## '.js'  : 'WHITESPACE_ONLY --formatting PRETTY_PRINT --debug',
                #'.js'    : bde('V0hJVEVTUEFDRV9PTkxZIC0tZm9ybWF0dGluZyBQUkVUVFlfUFJJTlQgLS1kZWJ1Zw=='),
                ##'.css' : 'DEBUG --pretty-print'
                #'.css' : bde('REVCVUcgLS1wcmV0dHktcHJpbnQ=')
            #}
        #else:
        map_nivel_compresor = {
            #'.js'    : 'ADVANCED_OPTIMIZATIONS',
            '.js'  : bde('QURWQU5DRURfT1BUSU1JWkFUSU9OUw=='),
            #'.css' : 'CLOSURE'
            '.css' : bde('Q0xPU1VSRQ==')
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
            renam = bde('Z29vZy5nZXRDc3NOYW1l')
            # Css
            renom = bde('Z3ouQ3Nz')
            f_entrada.write(int_cod + compilado.replace(renom, renam))

        if '.js' == sufijo:
            if args.depurar:
                # '--formatting PRETTY_PRINT'
                depurar = ' ' + bde('LS1mb3JtYXR0aW5nIFBSRVRUWV9QUklOVA==')
                if '2' == args.depurar:
                    # '--debug'
                    #depurar += ' ' + bde('LS1kZWJ1Zw==')
                    # 'SIMPLE_OPTIMIZATIONS'
                    nivel_compresor = bde('U0lNUExFX09QVElNSVpBVElPTlM=')

                compresor += depurar

            if args.externas:
                for ext in args.externas:
                    compresor += ' --externs %s' % os.path.join(dir_dependencias,
                                                                ext + sufijo)

            # compresor += ' --use_types_for_optimization '
            compresor += bde('IC0tdXNlX3R5cGVzX2Zvcl9vcHRpbWl6YXRpb24g')

        os.system(compresor % {
            'compresor' : ruta_compresor,
            'entrada'   : entrada_tmp_f,
            'salida'    : salida_tmp_f,
            'mapa'      : map_nom,
            'nivel'     : nivel_compresor
        })

        if '.css' == sufijo:
            import simplejson as json
            import re
            map_s = ''
            with open(map_nom, 'r') as map_f:
                map_s = map_f.read().replace(' ', '').replace('\n', '')
            with open(map_nom, 'w') as map_f:
                map_f.write(map_s)
            map_d = json.loads(map_s[23:-2])

            with open(salida_tmp_f, 'r', 'utf-8') as f_salida_tmp:
                salida_tmp = f_salida_tmp.read()


            # base = r'\[class.="%s([a-zA-Z]+)-"\]'
            base = bde('XFtjbGFzcy49IiVzKFthLXpBLVpdKyktIlxd')
            bse = base % ''
            bce = base % ' '

            # borig = r'\[class(.)="%s(%s)-"\]'
            # bdest = r'[class\1="%s%s-"]'
            borig = bde('XFtjbGFzcyguKT0iJXMoJXMpLSJcXQ==')
            bdest = bde('W2NsYXNzXDE9IiVzJXMtIl0=')
            bose = borig % ('', '%s')
            boce = borig % (' ', '%s')
            bdse = bdest % ('', '%s')
            bdce = bdest % (' ', '%s')


            classes = set(re.findall(bse, salida_tmp))
            for style in classes:
                salida_tmp = re.sub(bose % style,
                                    bdse % map_d[style],
                                    salida_tmp)
            classes = set(re.findall(bce, salida_tmp))
            for style in classes:
                salida_tmp = re.sub(boce % style,
                                    bdce % map_d[style],
                                    salida_tmp)


            with open(salida_tmp_f, 'w', 'utf-8') as f_salida_tmp:
                f_salida_tmp.write(salida_tmp)

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
            args.externas.append(bde('YmFzZQ=='))
            with open(salida_tmp_f, 'w') as f_sal:
                int_cod = depender(args.internas, dir_dependencias)

                #with open('renaming_map.js', 'r') as f_rem:
                #with open(bde('cmVuYW1pbmdfbWFwLmpz'), 'r') as f_rem:

                # with open(map_nom, 'r') as f_rem:
                #     f_sal.write(f_rem.read() \
                #                     .replace(' ', '') \
                #                     .replace('\n', '')
                #                 + int_cod.encode('utf-8') + compilado \
                #                     #.replace('gz.Css', 'gzc.Css') \
                #                     #.replace(bde('Z3ouQ3Nz'), bde('Z3pjLkNzcw==')) \
                #                     .encode('utf-8'))
                f_sal.write((int_cod + compilado).encode('utf-8'))
        elif '.css' == sufijo:
            entrada_tmp_f = os.path.join(tmp_b, f_nom)

            # with open(entrada_tmp_f, 'w', 'utf-8') as f_entrada:
            #     int_cod = depender(args.internas, dir_dependencias)
            #     # getCssName
            #     renam = bde('Z29vZy5nZXRDc3NOYW1l')
            #     # Css
            #     renom = bde('Z3ouQ3Nz')
            #     f_entrada.write(int_cod + compilado.replace(renom, renam))

            # compresor = bde('amF2YSAtamFyICUoY29tcHJlc29yKXMgLS1vdXRwdXQtZmlsZSAlKHNhbGlkYSlzIC0tb3V0cHV0LXJlbmFtaW5nLW1hcC1mb3JtYXQgQ0xPU1VSRV9DT01QSUxFRCAtLXJlbmFtZSAlKG5pdmVsKXMgLS1vdXRwdXQtcmVuYW1pbmctbWFwICUobWFwYSlzIC0tYWxsb3ctdW5yZWNvZ25pemVkLWZ1bmN0aW9ucyAtLWFsbG93LXVucmVjb2duaXplZC1wcm9wZXJ0aWVzICUoZW50cmFkYSlz')
            # os.system(compresor % {
            #     'compresor' : args.compresor_css,
            #     'entrada'   : entrada_tmp_f,
            #     'salida'    : salida_tmp_f,
            #     'mapa'      : map_nom,
            #     'nivel'     : 'DEBUG'
            # })

            # os.remove(entrada_tmp_f)
            # sys.exit(0)

            with open(salida_tmp_f, 'w') as f_sal:
                int_cod = depender(args.internas, dir_dependencias)
                f_sal.write((int_cod + compilado).encode('utf-8'))
            # sys.exit(0)

            #os.rename(entrada_tmp_f, )


            # with open(map_nom, 'w') as map_f:
            #     #map_f.write('goog.setCssNameMapping({});')
            #     map_f.write(bde('Z29vZy5zZXRDc3NOYW1lTWFwcGluZyh7fSk7'))
            #     int_cod = depender(args.internas, dir_dependencias)
            #     compilado = int_cod + compilado


        args.depurar = '1'

    ext_cod = depender(args.externas, dir_dependencias) if args.externas else ''

    derechos = bde('LyoqCiAqIENhdmFTb2Z0IFNBQyBodHRwOi8vY2F2YXNvZnRzYWMuY29tCiAqIGNyaXN0SGlhbiBHei4gKGdjY2EpIC0gaHR0cDovL2djY2EudGsKICovCg==')

    with open(salida_f, 'w', 'utf-8') as f_salida:
        with open(salida_tmp_f, 'r', 'utf-8') as f_salida_tmp:
            # salida = '(function(){%s}).call(this);' % f_salida_tmp.read()[:-1]
            salida_read  = f_salida_tmp.read()[:-1]
            salida = bde('KGZ1bmN0aW9uKCl7JXN9KS5jYWxsKHRoaXMpOw==') % salida_read if '.js' == sufijo else salida_read
            compilado = (ext_cod.replace('\n', ' ') + salida) \
                if args.depurar \
                else (ext_cod + salida).replace('\n', ' ')
            f_salida.write(derechos + compilado)

    os.remove(salida_tmp_f)
