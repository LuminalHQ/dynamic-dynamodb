# -*- coding: utf-8 -*-
""" Module with various calculators """
import math

from dynamic_dynamodb.log_handler import LOGGER as logger
from dynamic_dynamodb.config_handler import get_gsi_option
from dynamic_dynamodb import calculators


def decrease_reads_in_percent(
        current_provisioning, percent, table_name, table_key,
        gsi_name, gsi_key):
    """ Decrease the current_provisioning with percent %

    :type current_provisioning: int
    :param current_provisioning: The current provisioning
    :type percent: int
    :param percent: How many percent should we decrease with
    :type table_name: str
    :param table_name: Name of the DynamoDB table
    :type table_key: str
    :param table_key: Table configuration option key name
    :type gsi_name: str
    :param gsi_name: Name of the GSI
    :type gsi_key: str
    :param gsi_key: Name of the key
    :returns: int -- New provisioning value
    """
    decrease = int(float(current_provisioning)*(float(percent)/100))
    updated_provisioning = current_provisioning - decrease

    min_provisioned_reads = calculators.get_min_reads(
        current_provisioning,
        get_gsi_option(table_key, gsi_key, 'min_provisioned_reads'),
        '{0} - GSI: {1}'.format(table_name, gsi_name))

    if updated_provisioning < min_provisioned_reads:
        logger.info(
            '{0} - GSI: {1} - '
            'Reached provisioned reads min limit: {2:d}'.format(
                table_name, gsi_name, min_provisioned_reads))

        return min_provisioned_reads

    logger.debug(
        '{0} - GSI: {1} - '
        'Read provisioning will be decreased to {2:d} units'.format(
            table_name, gsi_name, updated_provisioning))

    return updated_provisioning


def increase_reads_in_percent(
        current_provisioning, percent, table_name, table_key,
        gsi_name, gsi_key):
    """ Increase the current_provisioning with percent %

    :type current_provisioning: int
    :param current_provisioning: The current provisioning
    :type percent: int
    :param percent: How many percent should we increase with
    :returns: int -- New provisioning value
    :type table_name: str
    :param table_name: Name of the DynamoDB table
    :type table_key: str
    :param table_key: Table configuration option key name
    :type gsi_name: str
    :param gsi_name: Name of the GSI
    :type gsi_key: str
    :param gsi_key: Name of the key
    """
    increase = int(math.ceil(float(current_provisioning)*(float(percent)/100)))
    updated_provisioning = current_provisioning + increase

    if get_gsi_option(table_key, gsi_key, 'max_provisioned_reads') > 0:
        if (updated_provisioning > get_gsi_option(
                table_key, gsi_key, 'max_provisioned_reads')):

            logger.info(
                '{0} - GSI: {1} - '
                'Reached provisioned reads max limit: {2:d}'.format(
                    table_name,
                    gsi_name,
                    int(get_gsi_option(
                        table_key, gsi_key, 'max_provisioned_reads'))))

            return get_gsi_option(
                table_key, gsi_key, 'max_provisioned_reads')

    logger.debug(
        '{0} - GSI: {1} - '
        'Read provisioning will be increased to {2:d} units'.format(
            table_name,
            gsi_name,
            updated_provisioning))

    return updated_provisioning


def decrease_writes_in_percent(
        current_provisioning, percent, table_name, table_key,
        gsi_name, gsi_key):
    """ Decrease the current_provisioning with percent %

    :type current_provisioning: int
    :param current_provisioning: The current provisioning
    :type percent: int
    :param percent: How many percent should we decrease with
    :type table_name: str
    :param table_name: Name of the DynamoDB table
    :type table_key: str
    :param table_key: Table configuration option key name
    :type gsi_name: str
    :param gsi_name: Name of the GSI
    :type gsi_key: str
    :param gsi_key: Name of the key
    :returns: int -- New provisioning value
    """
    decrease = int(float(current_provisioning)*(float(percent)/100))
    updated_provisioning = current_provisioning - decrease
    min_provisioned_writes = calculators.get_min_writes(
        current_provisioning,
        get_gsi_option(table_key, gsi_key, 'min_provisioned_writes'),
        '{0} - GSI: {1}'.format(table_name, gsi_name))

    if updated_provisioning < min_provisioned_writes:
        logger.info(
            '{0} - GSI: {1} - '
            'Reached provisioned writes min limit {2:d}'.format(
                table_name,
                gsi_name,
                min_provisioned_writes))

        return min_provisioned_writes

    logger.debug(
        '{0} - GSI: {1} - '
        'Write provisioning will be decreased to {2:d} units'.format(
            table_name,
            gsi_name,
            updated_provisioning))

    return updated_provisioning


def increase_writes_in_percent(
        current_provisioning, percent, table_name, table_key,
        gsi_name, gsi_key):
    """ Increase the current_provisioning with percent %

    :type current_provisioning: int
    :param current_provisioning: The current provisioning
    :type percent: int
    :param percent: How many percent should we increase with
    :type table_name: str
    :param table_name: Name of the DynamoDB table
    :type table_key: str
    :param table_key: Table configuration option key name
    :type gsi_name: str
    :param gsi_name: Name of the GSI
    :type gsi_key: str
    :param gsi_key: Name of the key
    :returns: int -- New provisioning value
    """
    increase = int(math.ceil(float(current_provisioning)*(float(percent)/100)))
    updated_provisioning = current_provisioning + increase

    if get_gsi_option(table_key, gsi_key, 'max_provisioned_writes'):
        max_provisioned_writes = int(get_gsi_option(
            table_key, gsi_key, 'max_provisioned_writes'))
    else:
        max_provisioned_writes = 0

    if (max_provisioned_writes > 0 and
            updated_provisioning > max_provisioned_writes):

            logger.info(
                '{0} - GSI: {1} - '
                'Reached provisioned writes max limit: {2:d}'.format(
                    table_name,
                    gsi_name,
                    max_provisioned_writes))

            return max_provisioned_writes

    logger.debug(
        '{0} - GSI: {1}'
        'Write provisioning will be increased to {2:d} units'.format(
            table_name,
            gsi_name,
            updated_provisioning))

    return updated_provisioning


def decrease_reads_in_units(
        current_provisioning, units, table_name, table_key, gsi_name, gsi_key):
    """ Decrease the current_provisioning with units units

    :type current_provisioning: int
    :param current_provisioning: The current provisioning
    :type units: int
    :param units: How many units should we decrease with
    :type table_name: str
    :param table_name: Name of the DynamoDB table
    :type table_key: str
    :param table_key: Table configuration option key name
    :type gsi_name: str
    :param gsi_name: Name of the GSI
    :type gsi_key: str
    :param gsi_key: Name of the key
    :returns: int -- New provisioning value
    """
    updated_provisioning = int(current_provisioning) - int(units)
    min_provisioned_reads = calculators.get_min_reads(
        current_provisioning,
        get_gsi_option(table_key, gsi_key, 'min_provisioned_reads'),
        '{0} - GSI: {1}'.format(table_name, gsi_name))

    if updated_provisioning < min_provisioned_reads:
        logger.info(
            '{0} - GSI: {1} - '
            'Reached provisioned reads min limit: {2:d}'.format(
                table_name,
                gsi_name,
                min_provisioned_reads))

        return min_provisioned_reads

    logger.debug(
        '{0} - GSI: {1} - '
        'Read provisioning will be decreased to {2:d} units'.format(
            table_name,
            gsi_name,
            updated_provisioning))

    return updated_provisioning


def increase_reads_in_units(
        current_provisioning, units, table_name, table_key, gsi_name, gsi_key):
    """ Increase the current_provisioning with units units

    :type current_provisioning: int
    :param current_provisioning: The current provisioning
    :type units: int
    :param units: How many units should we increase with
    :type table_name: str
    :param table_name: Name of the DynamoDB table
    :type table_key: str
    :param table_key: Table configuration option key name
    :type gsi_name: str
    :param gsi_name: Name of the GSI
    :type gsi_key: str
    :param gsi_key: Name of the key
    :returns: int -- New provisioning value
    """
    updated_provisioning = 0

    if int(units) > int(current_provisioning):
        updated_provisioning = 2 * int(current_provisioning)
    else:
        updated_provisioning = int(current_provisioning) + int(units)

    if get_gsi_option(table_key, gsi_key, 'max_provisioned_reads'):
        max_provisioned_reads = int(get_gsi_option(
            table_key, gsi_key, 'max_provisioned_reads'))
    else:
        max_provisioned_reads = 0

    if (max_provisioned_reads > 0 and
            updated_provisioning > max_provisioned_reads):
            logger.info(
                '{0} - GSI: {1} - '
                'Reached provisioned reads max limit: {2:d}'.format(
                    table_name,
                    gsi_name,
                    max_provisioned_reads))

            return max_provisioned_reads

    logger.debug(
        '{0} - GSI: {1} - '
        'Read provisioning will be increased to {2:d} units'.format(
            table_name,
            gsi_name,
            updated_provisioning))

    return updated_provisioning


def decrease_writes_in_units(
        current_provisioning, units, table_name, table_key, gsi_name, gsi_key):
    """ Decrease the current_provisioning with units units

    :type current_provisioning: int
    :param current_provisioning: The current provisioning
    :type units: int
    :param units: How many units should we decrease with
    :type table_name: str
    :param table_name: Name of the DynamoDB table
    :type table_key: str
    :param table_key: Table configuration option key name
    :type gsi_name: str
    :param gsi_name: Name of the GSI
    :type gsi_key: str
    :param gsi_key: Name of the key
    :returns: int -- New provisioning value
    """
    updated_provisioning = int(current_provisioning) - int(units)
    min_provisioned_writes = calculators.get_min_writes(
        current_provisioning,
        get_gsi_option(table_key, gsi_key, 'min_provisioned_writes'),
        '{0} - GSI: {1}'.format(table_name, gsi_name))

    if updated_provisioning < min_provisioned_writes:
        logger.info(
            '{0} - GSI: {1} - '
            'Reached provisioned writes min limit: {2:d}'.format(
                table_name,
                gsi_name,
                min_provisioned_writes))

        return min_provisioned_writes

    logger.debug(
        '{0} - GSI: {1} - '
        'Write provisioning will be decreased to {2:d} units'.format(
            table_name,
            gsi_name,
            updated_provisioning))

    return updated_provisioning


def increase_writes_in_units(
        current_provisioning, units, table_name, table_key, gsi_name, gsi_key):
    """ Increase the current_provisioning with units units

    :type current_provisioning: int
    :param current_provisioning: The current provisioning
    :type units: int
    :param units: How many units should we increase with
    :type table_name: str
    :param table_name: Name of the DynamoDB table
    :type table_key: str
    :param table_key: Table configuration option key name
    :type gsi_name: str
    :param gsi_name: Name of the GSI
    :type gsi_key: str
    :param gsi_key: Name of the key
    :returns: int -- New provisioning value
    """
    updated_provisioning = 0
    if int(units) > int(current_provisioning):
        updated_provisioning = 2 * int(current_provisioning)
    else:
        updated_provisioning = int(current_provisioning) + int(units)

    if get_gsi_option(table_key, gsi_key, 'max_provisioned_writes') > 0:
        if (updated_provisioning > get_gsi_option(
                table_key, gsi_key, 'max_provisioned_writes')):

            logger.info(
                '{0} - GSI: {1} - '
                'Reached provisioned writes max limit: {2:d}'.format(
                    table_name,
                    gsi_name,
                    int(get_gsi_option(
                        table_name, gsi_key, 'max_provisioned_writes'))))

            return get_gsi_option(
                table_key, gsi_key, 'max_provisioned_writes')

    logger.debug(
        '{0} - GSI: {1} - '
        'Write provisioning will be increased to {2:d} units'.format(
            table_name,
            gsi_name,
            updated_provisioning))

    return updated_provisioning
