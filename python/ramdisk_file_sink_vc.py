#!/usr/bin/env python
# -*- coding: utf-8 -*-
# gr-corrsounder
# Copyright (C) 2017  hf-ag
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# gr-corrsounder  Copyright (C) 2017  hf-ag
# This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
# This is free software, and you are welcome to redistribute it
# under certain conditions; type `show c' for details.

from gnuradio import gr, blocks
import os
import subprocess
import shlex
import getpass
import numpy as np
import psutil

class ctrl_progress(gr.sync_block):

    def __init__(self, filename, filesize, filesink):
        gr.sync_block.__init__(
            self, "Control Progress",
            in_sig=[(np.complex64, 1)],
            out_sig=[(np.float32, 1), (np.float32, 1), (np.float32, 1), (np.float32, 1)],
        )

        ##################################################
        # Variables
        ##################################################
        self.filesize = filesize
        self.filename = filename
        self.filesink = filesink

        self.acq_size = 0
        self.acq_done = False
        self.acquire_progress = 0.

        self.storage_done = False
        self.storage_progress = 0.

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out0 = output_items[0]
        out1 = output_items[1]
        out2 = output_items[2]
        out3 = output_items[3]

        ramdiskpath = "/tmp/ramdisk/capture.dat"

        if self.acq_done == False:
            if os.path.exists(ramdiskpath):
                # In case file size doesn't change
                if self.acq_size == os.path.getsize(ramdiskpath):
                    print "Finished acquistion! Starting storage progress..."
                    # Non-blocking process call
                    subprocess.Popen(shlex.split("cp " + ramdiskpath + ".hdr " + self.filename + ".hdr"))
                    self.copy_process = subprocess.Popen(shlex.split("cp "+ramdiskpath+" "+self.filename))
                    self.acquire_progress = 1.
                    self.acq_done = True
                else:
                    self.acq_size = os.path.getsize(ramdiskpath)
                    self.acquire_progress = float(self.acq_size) / float(self.filesize)

        if self.acq_done == True and self.storage_done == False:
            if os.path.exists(self.filename):
                self.storage_progress = float(os.path.getsize(self.filename)) / float(self.acq_size)

            if self.copy_process.poll() is not None:
                print "Finished storage!"
                self.storage_done = True
                self.storage_progress = 1.

        out0[:] = self.acquire_progress
        out1[:] = self.storage_progress
        out2[:] = psutil.cpu_percent(interval=None)
        vmem = psutil.virtual_memory()
        out3[:] = vmem.percent
        return len(output_items[0])

    def stop(self):
        print "Removing ramdisk..."
        getpass.getuser()
        ps = subprocess.Popen(shlex.split("sudo rm /tmp/ramdisk/*"))
        if ps.wait() == 0:
            ps = subprocess.Popen(shlex.split("sudo umount /tmp/ramdisk"))
            if ps.wait() == 0:
                ps = subprocess.Popen(shlex.split("sudo rmdir /tmp/ramdisk/"))
                if ps.wait() == 0:
                    print "Ramdisk successfully removed!"
                    return True

        print "Warning: Removing ramdisk failed! Please run the following commands:"
        print "    sudo rm /tmp/ramdisk/*"
        print "    sudo umount /tmp/ramdisk"
        print "    sudo rmdir /tmp/ramdisk/"
        return False


class ramdisk_file_sink_vc(gr.hier_block2):

    def __init__(self, filename, filesize = 100e6):
        gr.hier_block2.__init__(
            self, "Ramdisk File Sink",
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
            gr.io_signaturev(4, 4, [gr.sizeof_float*1, gr.sizeof_float*1, gr.sizeof_float*1, gr.sizeof_float*1]),
        )

        ##################################################
        # Variables
        ##################################################
        mem = psutil.virtual_memory()
        self.filesize = int(min(mem.free - 500e6, filesize))
        print "Actual file size: " + str(filesize)
        print "Set file size: " + str(self.filesize)
        self.filename = filename

        # Create RAMDISK
        subprocess.call(shlex.split("sudo mkdir /tmp/ramdisk"))
        subprocess.call(shlex.split("sudo mount -t tmpfs -o size=" + str(int(self.filesize)) + " none /tmp/ramdisk"))
        username = getpass.getuser()
        subprocess.call(shlex.split("sudo chown -R " + username + ":" + username + " /tmp/ramdisk"))

        ##################################################
        # Blocks
        ##################################################
        self.decim = blocks.keep_one_in_n(gr.sizeof_gr_complex * 1, int(self.filesize / 8 / 100))
        self.file_meta_sink = blocks.file_meta_sink(gr.sizeof_gr_complex * 1, "/tmp/ramdisk/capture.dat", 1, 1, blocks.GR_FILE_FLOAT, True, 1000000, "", True)
        self.file_meta_sink.set_unbuffered(False)
        self.ctrl_progress = ctrl_progress(filename=filename, filesize=self.filesize, filesink=self.file_meta_sink)

        ##################################################
        # Connections
        ##################################################
        self.connect((self, 0), (self.file_meta_sink, 0))
        self.connect((self, 0), (self.decim, 0))
        self.connect((self.decim, 0), (self.ctrl_progress, 0))
        self.connect((self.ctrl_progress, 0), (self, 0))
        self.connect((self.ctrl_progress, 1), (self, 1))
        self.connect((self.ctrl_progress, 2), (self, 2))
        self.connect((self.ctrl_progress, 3), (self, 3))
