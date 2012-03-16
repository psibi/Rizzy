#!/usr/bin/env python

# stepic - Python image steganography
# Copyright (C) 2007 Lenny Domnitser
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


import optparse
import sys
import traceback
import Image
import stepic


def encode_files(image_in, data_in, image_out, format):
    image = Image.open(image_in)
    if not hasattr(data_in, 'read'):
        data_in = open(data_in, 'rb')
    data = data_in.read()
    if hasattr(image_out, 'write'):
        format = image.format
    stepic.encode_inplace(image, data)
    image.save(image_out, format)


def decode_files(image_in, data_out):
    image = Image.open(image_in)
    if not hasattr(data_out, 'write'):
        data_out = open(data_out, 'wb')
    data_out.write(stepic.decode(image))


def main():
    parser = optparse.OptionParser(version=stepic.__version__,
                                   description='Steganographically hide data in a bitmap-style image, or read hidden data from an image')
    parser.add_option('--debug', action='store_true', default=False)
    parser.add_option('-d', '--decode', action='store_true', default=False,
                      help='given an image, write out the hidden data file')
    parser.add_option('-e', '--encode', action='store_true', default=False,
                      help='given an image and data file, write out a new image file with the data hidden in it')
    parser.add_option('-f', '--format', metavar='FORMAT',
                      help='output image format (PNG recommended, defaults to input format)')
    parser.add_option('-i', '--image-in=', dest='image_in', metavar='FILE', default=sys.stdin,
                      help='read in image FILE for decoding or encoding')
    parser.add_option('-t', '--data-in=', dest='data_in', metavar='FILE', default=sys.stdin,
                      help='read in data FILE for encoding')
    parser.add_option('-o', '--out=', dest='out', metavar='FILE', default=sys.stdout,
                      help='write out to FILE, data when decoding, image when encoding')
    options, args = parser.parse_args()

    if args:
        parser.print_usage()
        sys.exit(2)
    if options.decode == options.encode:
        parser.print_usage()
        print >> sys.stderr, 'choose either encode or decode'

    try:
        if options.decode:
            decode_files(options.image_in, options.out)
        elif options.encode:
            encode_files(options.image_in, options.data_in, options.out, options.format)
    except (TypeError, ValueError), e:
        print >> sys.stderr, 'error:', e
        sys.exit(1)
    except KeyboardInterrupt:
        pass
    except Exception, e:
        print >> sys.stderr, '%s: %s' % (e.__class__.__name__, e)
        if options.debug:
            traceback.print_tb(sys.exc_traceback)
        sys.exit(3)


if __name__ == '__main__':
    main()
