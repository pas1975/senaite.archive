# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.ARCHIVE.
#
# SENAITE.ARCHIVE is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2021 by it's authors.
# Some rights reserved, see README and LICENSE.

import logging
from AccessControl.Permission import addPermission
from AccessControl.SecurityInfo import ModuleSecurityInfo
from senaite.archive import permissions
from senaite.archive.config import PRODUCT_NAME
from senaite.archive.config import PRODUCT_TYPES
from senaite.archive.interfaces import ISenaiteArchiveLayer
from zope.i18nmessageid import MessageFactory

from bika.lims import api

security = ModuleSecurityInfo(PRODUCT_NAME)
messageFactory = MessageFactory(PRODUCT_NAME)
logger = logging.getLogger(PRODUCT_NAME)


def is_installed():
    """Returns whether the product is installed or not
    """
    request = api.get_request()
    return ISenaiteArchiveLayer.providedBy(request)


def check_installed(default_return):
    """Decorator to prevent the function to be called if product not installed
    :param default_return: value to return if not installed
    """
    def is_installed_decorator(func):
        def wrapper(*args, **kwargs):
            if not is_installed():
                return default_return
            return func(*args, **kwargs)
        return wrapper
    return is_installed_decorator


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    logger.info("*** Initializing SENAITE ARCHIVE Customization package ***")

    # Set add permissions
    for typename in PRODUCT_TYPES:
        permission_id = "Add" + typename
        permission_name = getattr(permissions, permission_id)
        security.declarePublic(permission_id)
        addPermission(permission_name, default_roles=("Manager", ))
