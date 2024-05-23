import os
from pathlib import Path
import gc
import traceback
import logging
from fnmatch import fnmatch

import pydicom
import dicom2nifti.common as common
import dicom2nifti.convert_dicom as convert_dicom
import dicom2nifti.settings
from dicom2nifti.convert_dir import _remove_accents, _is_valid_imaging_dicom


def convert_directory(dicom_directory, output_folder, description_filter="ALL", compression=True, reorient=True, logger: logging.Logger = None):
    """
    Modified from `dicom2nifti.convert_directory`

    Args:
        description_filter: filter the `SeriesDescription` read with `pydicom.read_file` by `fnmatch(x.SeriesDescription, description_filter)`, will not filter if set to `ALL`
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    # sort dicom files by series uid
    dicom_series = {}
    for root, _, files in os.walk(dicom_directory):
        for dicom_file in files:
            file_path = os.path.join(root, dicom_file)
            # noinspection PyBroadException
            try:
                if common.is_dicom_file(file_path):
                    # read the dicom as fast as possible
                    # (max length for SeriesInstanceUID is 64 so defer_size 100 should be ok)

                    dicom_headers = pydicom.read_file(file_path,
                                                      defer_size="1 KB",
                                                      stop_before_pixels=False,
                                                      force=dicom2nifti.settings.pydicom_read_force)
                    if not _is_valid_imaging_dicom(dicom_headers):
                        logger.info("Skipping: %s" % file_path)
                        continue
                    logger.info("Organizing: %s" % file_path)
                    # add filter
                    if description_filter == "ALL" or fnmatch(dicom_headers.SeriesDescription, description_filter):
                        if dicom_headers.SeriesInstanceUID not in dicom_series:
                            dicom_series[dicom_headers.SeriesInstanceUID] = {"series": [], "dir_name": root.split("/")[-1], "file_head": dicom_file.split("_")[0]}
                        dicom_series[dicom_headers.SeriesInstanceUID]["series"].append(dicom_headers)
            except:  # Explicitly capturing all errors here to be able to continue processing all the rest
                logger.warning("Unable to read: %s" % file_path)
                traceback.print_exc()

    # start converting one by one
    for series_id, dicom_dict in dicom_series.items():
        dicom_input = dicom_dict["series"]
        base_filename = ""
        # noinspection PyBroadException
        try:
            # construct the filename for the nifti
            base_filename = ""
            if 'SeriesNumber' in dicom_input[0]:
                base_filename = _remove_accents('%s' % dicom_input[0].SeriesNumber)
                if 'SeriesDescription' in dicom_input[0]:
                    base_filename = _remove_accents('%s_%s' % (base_filename,
                                                               dicom_input[0].SeriesDescription))
                elif 'SequenceName' in dicom_input[0]:
                    base_filename = _remove_accents('%s_%s' % (base_filename,
                                                               dicom_input[0].SequenceName))
                elif 'ProtocolName' in dicom_input[0]:
                    base_filename = _remove_accents('%s_%s' % (base_filename,
                                                               dicom_input[0].ProtocolName))
            else:
                base_filename = _remove_accents(dicom_input[0].SeriesInstanceUID)
            # add DICOM dir_name and file_head to the filename
            base_filename = f"{dicom_dict['dir_name']}_{dicom_dict['file_head']}_{base_filename}"
            logger.info('--------------------------------------------')
            logger.info('Start converting %s' % base_filename)
            if compression:
                nifti_file = os.path.join(output_folder, base_filename + '.nii.gz')
            else:
                nifti_file = os.path.join(output_folder, base_filename + '.nii')
            convert_dicom.dicom_array_to_nifti(dicom_input, nifti_file, reorient)
            gc.collect()
        except:  # Explicitly capturing app exceptions here to be able to continue processing
            logger.info("Unable to convert: %s" % base_filename)
            traceback.print_exc()


def convert_subject(dicom_directory, output_folder, description_filter="ALL", compression=True, reorient=True, logger: logging.Logger = None):
    if logger is None:
        logger = logging.getLogger(__name__)
    
    dicom_directory = Path(dicom_directory)
    output_folder = Path(output_folder)

    dicom_series = {}
    for file_path in dicom_directory.iterdir():
        try:
            if common.is_dicom_file(file_path):
                # read the dicom as fast as possible
                # (max length for SeriesInstanceUID is 64 so defer_size 100 should be ok)

                dicom_headers = pydicom.read_file(file_path,
                                                  defer_size="1 KB",
                                                  stop_before_pixels=False,
                                                  force=dicom2nifti.settings.pydicom_read_force)
                if not _is_valid_imaging_dicom(dicom_headers):
                    logger.info("Skipping: %s" % file_path)
                    continue
                logger.info("Organizing: %s" % file_path)
                # add filter
                if description_filter == "ALL" or fnmatch(dicom_headers.SeriesDescription, description_filter):
                    if dicom_headers.SeriesInstanceUID not in dicom_series:
                        dicom_series[dicom_headers.SeriesInstanceUID] = {"series": [], "dir_name": file_path.parent.name, "file_head": file_path.name.split("_")[0]}
                    dicom_series[dicom_headers.SeriesInstanceUID]["series"].append(dicom_headers)
        except:  # Explicitly capturing all errors here to be able to continue processing all the rest
            logger.warning("Unable to read: %s" % file_path)
            traceback.print_exc()
    
    # start converting one by one
    for series_id, dicom_dict in dicom_series.items():
        dicom_input = dicom_dict["series"]
        base_filename = ""
        # noinspection PyBroadException
        try:
            # construct the filename for the nifti
            base_filename = ""
            if 'SeriesNumber' in dicom_input[0]:
                base_filename = _remove_accents('%s' % dicom_input[0].SeriesNumber)
                if 'SeriesDescription' in dicom_input[0]:
                    base_filename = _remove_accents('%s_%s' % (base_filename,
                                                               dicom_input[0].SeriesDescription))
                elif 'SequenceName' in dicom_input[0]:
                    base_filename = _remove_accents('%s_%s' % (base_filename,
                                                               dicom_input[0].SequenceName))
                elif 'ProtocolName' in dicom_input[0]:
                    base_filename = _remove_accents('%s_%s' % (base_filename,
                                                               dicom_input[0].ProtocolName))
            else:
                base_filename = _remove_accents(dicom_input[0].SeriesInstanceUID)
            # add DICOM dir_name and file_head to the filename
            base_filename = f"{dicom_dict['dir_name']}_{dicom_dict['file_head']}_{base_filename}"
            logger.info('--------------------------------------------')
            logger.info('Start converting %s' % base_filename)
            if compression:
                nifti_file = os.path.join(output_folder, base_filename + '.nii.gz')
            else:
                nifti_file = os.path.join(output_folder, base_filename + '.nii')
            convert_dicom.dicom_array_to_nifti(dicom_input, nifti_file, reorient)
            gc.collect()
        except:  # Explicitly capturing app exceptions here to be able to continue processing
            logger.info("Unable to convert: %s" % base_filename)
            traceback.print_exc()
