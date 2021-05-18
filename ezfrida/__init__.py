import argparse
import frida
import os
import sys
import pkg_resources

from ezfrida.logging import setup_logging
from pathlib import Path


logger = None

def parse_args(print_help=False):
    argparser = argparse.ArgumentParser(prog='ezfrida')
    argparser.add_argument('-a', '--attach', help='process to attach to', default=None, required=True)
    argparser.add_argument('-l', '--log', help='log output to file', action='store_true')
    argparser.add_argument('-d', '--debug', help='enable debug logging', action='store_true')
    argparser.add_argument('-s', '--scripts', help='internal Frida scripts to include, comma separated', default=None, required=True)
    argparser.add_argument('-tc', '--target-class', help='Class to target with applicable scripts', default=None)
    args = argparser.parse_args()
    if print_help:
        return argparser.print_help()
    else:
        return args


def on_message(message, data):
    if message['type'] == 'send':
        logger.info(message['payload'])
    else:
        logger.error(message)


def js_builder():
    """
    I'm certain there is a much smarter way of building this out
    and I'm sure I'll do it sooner or later.
    """
    jscript = 'Java.perform(function() {'
    scripts = args.scripts.replace('"', '')
    scripts = list(scripts.split(','))
    for script in scripts:
        logger.debug(script)
        jscript_dir = pkg_resources.resource_filename(__name__, 'res/javascript')
        logger.debug(jscript_dir)
        for root, dirs, files in os.walk(jscript_dir):
            logger.debug("looking in %s" % root)
            if script in files:
                script = os.path.join(root, script)
                with open(script) as f:
                    _f = f.read()
                    logger.debug("Found!\n%s" % _f)
                    jscript += '\n%s' % _f
            else:
                logger.debug('Script %s not found in %s! Skipping...' % (script, root))
    jscript += '\n});'
    logger.debug("\n%s" % jscript)
    # jscript = jscript.replace('${{PROCESS_NAME}}', args.attach)
    return jscript


def main():
    global args
    args = parse_args()
    print("Enable logging: %s" % args.log)
    global logger
    logger = setup_logging(log_to_file=args.log, debug=args.debug)
    logger.info("Starting EZFrida")
    if args.attach:
        process = frida.get_usb_device().attach(args.attach)
        jscript = js_builder()
        script = process.create_script(jscript)
        script.on('message', on_message)
        script.load()
        sys.stdin.read()
    else:
        logger.critical("NO PROCESS TO ATTACH TO! Exiting...")