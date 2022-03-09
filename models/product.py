# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)

BARCODE_PREFIX = "21"
EAN13_LENGTH = 13

class Product(models.Model):
    _inherit = "product.product"
    
    def barcode_with_qty(self, product_qty):
        _logger.info(f"original product barcode is {self.barcode}")
        
        if len(str(self.barcode)) == EAN13_LENGTH and self.barcode.startswith(BARCODE_PREFIX):
            reference = str(self.barcode[2:7])
            qty = str(int(product_qty))
            qty_decimal = str(product_qty).split(".")[1]
            barcode = f"{BARCODE_PREFIX}{reference.zfill(5)}{qty.zfill(3)}{qty_decimal.ljust(2, '0')}"
            checksum = self.env['barcode.nomenclature'].ean_checksum(barcode + "0")
            _logger.info(f"EAN check calculated as {checksum} for barcode {barcode} ")
            return barcode + str(checksum)
        else:
            _logger.info(f"barcode not starts with the provided prefix {BARCODE_PREFIX}")