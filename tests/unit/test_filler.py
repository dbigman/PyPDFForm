# -*- coding: utf-8 -*-

import os

import pdfrw
import pytest
from pdfrw.objects.pdfname import BasePdfName

from PyPDFForm.core import constants, filler, template
from PyPDFForm.middleware import constants as middleware_constants
from PyPDFForm.middleware import template as template_middleware
from PyPDFForm.middleware.element import ElementType


@pytest.fixture
def pdf_samples():
    return os.path.join(os.path.dirname(__file__), "..", "..", "pdf_samples")


@pytest.fixture
def template_stream(pdf_samples):
    with open(os.path.join(pdf_samples, "sample_template.pdf"), "rb+") as f:
        return f.read()


@pytest.fixture
def template_with_radiobutton_stream(pdf_samples):
    with open(
        os.path.join(pdf_samples, "sample_template_with_radio_button.pdf"), "rb+"
    ) as f:
        return f.read()


@pytest.fixture
def data_dict():
    return {
        "test": "test_1",
        "check": True,
        "test_2": "test_2",
        "check_2": False,
        "test_3": "test_3",
        "check_3": True,
    }


def test_fill(template_stream, data_dict):
    elements = template_middleware.build_elements(template_stream)

    for k, v in data_dict.items():
        if k in elements:
            elements[k].value = v

            if elements[k].type == ElementType.text:
                elements[k].font = middleware_constants.GLOBAL_FONT
                elements[k].font_size = middleware_constants.GLOBAL_FONT_SIZE
                elements[k].font_color = middleware_constants.GLOBAL_FONT_COLOR
                elements[k].text_x_offset = middleware_constants.GLOBAL_TEXT_X_OFFSET
                elements[k].text_y_offset = middleware_constants.GLOBAL_TEXT_Y_OFFSET
                elements[
                    k
                ].text_wrap_length = middleware_constants.GLOBAL_TEXT_WRAP_LENGTH
            elements[k].validate_constants()
            elements[k].validate_value()
            elements[k].validate_text_attributes()

    result_stream = filler.fill(template_stream, elements)

    assert result_stream != template_stream

    for element in template.iterate_elements(result_stream):
        key = template.get_element_key(element)

        assert element[constants.FIELD_FLAG_KEY] == pdfrw.PdfObject(1)

        if isinstance(data_dict[key], bool):
            assert element[constants.CHECKBOX_FIELD_VALUE_KEY] == (
                pdfrw.PdfName.Yes if data_dict[key] else pdfrw.PdfName.Off
            )


def test_fill_v2(template_stream, data_dict):
    elements = template_middleware.build_elements(template_stream)

    for k, v in data_dict.items():
        if k in elements:
            elements[k].value = v

            if elements[k].type == ElementType.text:
                elements[k].font = middleware_constants.GLOBAL_FONT
                elements[k].font_size = middleware_constants.GLOBAL_FONT_SIZE
                elements[k].font_color = middleware_constants.GLOBAL_FONT_COLOR
                elements[k].text_x_offset = middleware_constants.GLOBAL_TEXT_X_OFFSET
                elements[k].text_y_offset = middleware_constants.GLOBAL_TEXT_Y_OFFSET
                elements[
                    k
                ].text_wrap_length = middleware_constants.GLOBAL_TEXT_WRAP_LENGTH
            elements[k].validate_constants()
            elements[k].validate_value()
            elements[k].validate_text_attributes()

    result_stream = filler.fill_v2(template_stream, elements)
    assert result_stream != template_stream

    for element in template.iterate_elements(result_stream):
        key = template.get_element_key(element)

        assert element[constants.FIELD_FLAG_KEY] != pdfrw.PdfObject(1)

        if isinstance(data_dict[key], bool):
            assert element[constants.CHECKBOX_FIELD_VALUE_KEY] == pdfrw.PdfName.Off


def test_fill_sejda(sejda_template, sejda_data):
    elements = template_middleware.build_elements(sejda_template, sejda=True)

    for k, v in elements.items():
        if k in sejda_data:
            v.value = sejda_data[k]

        if elements[k].type == ElementType.text:
            elements[k].font = middleware_constants.GLOBAL_FONT
            elements[k].font_size = middleware_constants.GLOBAL_FONT_SIZE
            elements[k].font_color = middleware_constants.GLOBAL_FONT_COLOR
            elements[k].text_x_offset = middleware_constants.GLOBAL_TEXT_X_OFFSET
            elements[k].text_y_offset = middleware_constants.GLOBAL_TEXT_Y_OFFSET
            elements[k].text_wrap_length = middleware_constants.GLOBAL_TEXT_WRAP_LENGTH
        elements[k].validate_constants()
        elements[k].validate_value()
        elements[k].validate_text_attributes()

    result_stream = filler.fill(sejda_template, elements, sejda=True)

    assert result_stream != template_stream

    for element in template.iterate_elements(result_stream):
        assert element[constants.PARENT_KEY][
            constants.FIELD_FLAG_KEY
        ] == pdfrw.PdfObject(1)


def test_fill_sejda_v2(sejda_template, sejda_data):
    elements = template_middleware.build_elements(sejda_template, sejda=True)

    for k, v in elements.items():
        if k in sejda_data:
            v.value = sejda_data[k]

        if elements[k].type == ElementType.text:
            elements[k].font = middleware_constants.GLOBAL_FONT
            elements[k].font_size = middleware_constants.GLOBAL_FONT_SIZE
            elements[k].font_color = middleware_constants.GLOBAL_FONT_COLOR
            elements[k].text_x_offset = middleware_constants.GLOBAL_TEXT_X_OFFSET
            elements[k].text_y_offset = middleware_constants.GLOBAL_TEXT_Y_OFFSET
            elements[k].text_wrap_length = middleware_constants.GLOBAL_TEXT_WRAP_LENGTH
        elements[k].validate_constants()
        elements[k].validate_value()
        elements[k].validate_text_attributes()

    result_stream = filler.fill_v2(sejda_template, elements)

    assert result_stream != template_stream

    for element in template.iterate_elements(result_stream):
        assert element[constants.PARENT_KEY][
            constants.FIELD_FLAG_KEY
        ] != pdfrw.PdfObject(1)


def test_fill_with_radiobutton(template_with_radiobutton_stream, data_dict):
    elements = template_middleware.build_elements(template_with_radiobutton_stream)

    data_dict = {key: value for key, value in data_dict.items()}
    data_dict["radio_1"] = 0
    data_dict["radio_2"] = 1
    data_dict["radio_3"] = 2

    radio_button_tracker = {}

    for k, v in data_dict.items():
        if k in elements:
            elements[k].value = v

            if elements[k].type == ElementType.text:
                elements[k].font = middleware_constants.GLOBAL_FONT
                elements[k].font_size = middleware_constants.GLOBAL_FONT_SIZE
                elements[k].font_color = middleware_constants.GLOBAL_FONT_COLOR
                elements[k].text_x_offset = middleware_constants.GLOBAL_TEXT_X_OFFSET
                elements[k].text_y_offset = middleware_constants.GLOBAL_TEXT_Y_OFFSET
                elements[
                    k
                ].text_wrap_length = middleware_constants.GLOBAL_TEXT_WRAP_LENGTH
            elements[k].validate_constants()
            elements[k].validate_value()
            elements[k].validate_text_attributes()

    result_stream = filler.fill(template_with_radiobutton_stream, elements)

    assert result_stream != template_with_radiobutton_stream

    for element in template.iterate_elements(result_stream):
        key = template.get_element_key(element)

        if isinstance(data_dict[key], bool) or isinstance(data_dict[key], str):
            assert element[constants.FIELD_FLAG_KEY] == pdfrw.PdfObject(1)
        else:
            assert element[constants.PARENT_KEY][
                constants.FIELD_FLAG_KEY
            ] == pdfrw.PdfObject(1)

        if isinstance(data_dict[key], bool):
            assert element[constants.CHECKBOX_FIELD_VALUE_KEY] == (
                pdfrw.PdfName.Yes if data_dict[key] else pdfrw.PdfName.Off
            )
        elif isinstance(data_dict[key], int):
            if key not in radio_button_tracker:
                radio_button_tracker[key] = 0
            radio_button_tracker[key] += 1

            if data_dict[key] == radio_button_tracker[key] - 1:
                assert element[constants.CHECKBOX_FIELD_VALUE_KEY] == BasePdfName(
                    "/" + str(data_dict[key]), False
                )
            else:
                assert element[constants.CHECKBOX_FIELD_VALUE_KEY] == pdfrw.PdfName.Off


def test_simple_fill(template_stream, data_dict):
    result_stream = filler.simple_fill(template_stream, data_dict, False)

    assert result_stream != template_stream

    for element in template.iterate_elements(result_stream):
        key = template.get_element_key(element)

        if isinstance(data_dict[key], bool):
            assert element[constants.CHECKBOX_FIELD_VALUE_KEY] == (
                pdfrw.PdfName.Yes if data_dict[key] else pdfrw.PdfName.Off
            )
        else:
            assert element[constants.TEXT_FIELD_VALUE_KEY][1:-1] == data_dict[key]
        assert element[constants.FIELD_FLAG_KEY] == pdfrw.PdfObject(1)


def test_simple_fill_with_radiobutton(template_with_radiobutton_stream, data_dict):
    data_dict = {key: value for key, value in data_dict.items()}
    data_dict["radio_1"] = 0
    data_dict["radio_2"] = 1
    data_dict["radio_3"] = 2

    radio_button_tracker = {}

    result_stream = filler.simple_fill(
        template_with_radiobutton_stream, data_dict, True
    )

    assert result_stream != template_with_radiobutton_stream

    for element in template.iterate_elements(result_stream):
        key = template.get_element_key(element)

        if isinstance(data_dict[key], bool):
            assert element[constants.CHECKBOX_FIELD_VALUE_KEY] == (
                pdfrw.PdfName.Yes if data_dict[key] else pdfrw.PdfName.Off
            )
        elif isinstance(data_dict[key], int):
            if key not in radio_button_tracker:
                radio_button_tracker[key] = 0
            radio_button_tracker[key] += 1

            if data_dict[key] == radio_button_tracker[key] - 1:
                assert element[constants.CHECKBOX_FIELD_VALUE_KEY] == BasePdfName(
                    "/" + str(data_dict[key]), False
                )
            else:
                assert element[constants.CHECKBOX_FIELD_VALUE_KEY] == pdfrw.PdfName.Off
        else:
            assert element[constants.TEXT_FIELD_VALUE_KEY][1:-1] == data_dict[key]
        assert element[constants.FIELD_FLAG_KEY] != pdfrw.PdfObject(1)
