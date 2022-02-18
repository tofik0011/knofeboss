//#region CONSTANTS LET
const body = $('body');
let csrf = $("[name='csrfmiddlewaretoken']").val();
let menu = $('#menu');
let lng_changer = $('#lng_changer');
let lng_form = $('#lng_form');
let CITY_REF = null;
let CITY_NAME = null;
let DELIVERY_TYPE = null;
let OD_SETTLEMENT = null;
let NP_SETTLEMENT = null;
let NP_WAREHOUSE = null;


//#endregion CONSTANTS

//#region FUNCTIONS
function show_modal_testimonial() {
    $("#modal-testimonials").remove();
    return $.ajax({
        type: "POST",
        url: CONFIG_DATA.URLS.view__testimonials_model,
        success: (data) => {
            body.append(data);
            M.Modal.init(document.getElementById('modal-testimonials'))
            M.Modal.getInstance(document.getElementById('modal-testimonials')).open();
        }
    });
}

function add_testimonial() {
    let photo = null;
    if ($("#add_testimonials_attach_photo")[0].files.length > 0) {
        photo = $("#add_testimonials_attach_photo")[0].files[0]
    }
    let fd = new FormData;
    fd.append('author', $('#testimonials_author').val());
    fd.append('photo', photo);
    fd.append('text', $('#testimonials_comment').val());
    fd.append('rating', parseInt($('.testimonials_rating:checked').val(), 6));

    $.ajax({
        type: "POST",
        url: CONFIG_DATA.URLS.add_testimonial,
        data: fd,
        processData: false,
        contentType: false,
        success: function (data) {
            if (data.success === true) {
                swal({
                    icon: 'success',
                    className: 'custom_swal',
                    text: data.message,
                }).then(() => {
                    M.Modal.getInstance(document.getElementById('modal-testimonials')).close();
                });
            } else {
                swal({
                    className: 'custom_swal',
                    text: data.message,
                })
            }
        },
    });
}

function add_notification(data) {
    body.append(data);
    let notification = $('.notification');
    notification.animate({
        opacity: 100,
        top: "10px",
    }, 300);
    setTimeout(function () {
        notification.fadeOut(300, function () {
            notification.remove();
        });
    }, 5000);
}

body.on('click', '.notification .close_ntf', function (e) {
    e.preventDefault();
    $('.notification').fadeOut(300, function () {
        $('.notification').remove();
    });
});


function get_product_price_by_options(product_id) {
    let content = {
        "product_id": product_id,
        "product_options": get_selected_options(product_id, 'badges')
    };
    let result;
    $.ajax({
        type: "POST",
        url: CONFIG_DATA.URLS.get_product_price_by_options,
        data: {
            'data': JSON.stringify(content),
        },
        async: false,
        success: function (data) {
            result = data;
        }
    });
    return result;
}

//
// function mark_selected(obj) {
//     if ($(obj).hasClass('selected')) {
//         $(obj).removeClass('selected');
//         return true;
//     }
//     let option_id = $(obj).attr('data-option-id');
//     let product_id = $(obj).attr('data-product-id');
//     let option_value_id = $(obj).attr('data-value-id');
//     let kek = $('a[data-product-id="' + product_id + '"][data-option-id="' + option_id + '"]');
//     $.each(kek, function (key, value) {
//         $(value).removeClass('selected');
//     });
//     $(obj).addClass('selected');
// }

function convert_to_currency(old_price) {
    return parseFloat(old_price * CONFIG_DATA.CURRENCIES.CURRENT.value);
}

function convert_to_default(old_price) {
    return parseFloat(old_price / CONFIG_DATA.CURRENCIES.CURRENT.value);
}

function build_price_track() {
    let slider = document.getElementById('price-range');
    if (slider) {
        noUiSlider.create(slider, {
            // behaviour: 'tap',
            start: [parseFloat(CONFIG_DATA.VALUES.min_price), parseFloat(CONFIG_DATA.VALUES.max_price)],
            connect: true,
            animate: false,
            range: {
                min: parseFloat(CONFIG_DATA.VALUES.category_min_price), max: parseFloat(CONFIG_DATA.VALUES.category_max_price)
            }
        });
        slider.noUiSlider.on('update', function (values, handle) {
            let min_v = values[0]
            let max_v = values[1]
            $("#min-price").html(parseFloat(min_v).toFixed(2));
            $("#max-price").html(parseFloat(max_v).toFixed(2));
        });
        slider.noUiSlider.on('change', function (values) {
            let min_v = values[0]
            let max_v = values[1]
            $("#min-price").html(parseFloat(min_v).toFixed(2));
            $("#max-price").html(parseFloat(max_v).toFixed(2));
            update_url_filters();
        });
    }

    // var mySlider = new rSlider({
    //     target: '#price-range',
    //     values: {min: parseFloat(CONFIG_DATA.VALUES.category_min_price), max: parseFloat(CONFIG_DATA.VALUES.category_max_price)},
    //     range: true,
    //     tooltip: true,
    //     scale: false,
    //     labels: false,
    //     step: 1,
    //     set: [parseFloat(CONFIG_DATA.VALUES.min_price), parseFloat(CONFIG_DATA.VALUES.max_price)],
    //     onChange: function (values) {
    //         console.log(values);
    //         let min_v = values.split(',')[0]
    //         let max_v = values.split(',')[1]
    //         $("#min-price").html(parseFloat(min_v).toFixed(2));
    //         $("#max-price").html(parseFloat(max_v).toFixed(2));
    //         update_url_filters();
    //     },
    // })
    //
    // $(".rs-tooltip").hide();
    // $(".rs-scale").remove();
    // // $(".rs-container.rs-noscale").css("height", "25px");
    // $(".rs-tooltip").bind("DOMSubtreeModified", (e) => {
    //     console.log("test")
    //     let min_v = mySlider.getValue().split(',')[0]
    //     let max_v = mySlider.getValue().split(',')[1]
    //     $("#min-price").html(parseFloat(min_v).toFixed(2));
    //     $("#max-price").html(parseFloat(max_v).toFixed(2));
    // })
    // mySlider.onChange = (() => {
    //     let min_v = mySlider.getValue().split(',')[0]
    //     let max_v = mySlider.getValue().split(',')[1]
    //     $("#min-price").html(parseFloat(min_v).toFixed(2));
    //     $("#max-price").html(parseFloat(max_v).toFixed(2));
    //     // update_url_filters();
    //     console.log(min_v, max_v)
    // })
}

// function build_price_track() {
//     console.log('event build_price_track')
//     $("#min-price").html(CONFIG_DATA.VALUES.min_price);
//     $("#max-price").html(CONFIG_DATA.VALUES.max_price);
//     $("#price-range").slider({
//         range: true,
//         min: parseFloat(CONFIG_DATA.VALUES.category_min_price),
//         max: parseFloat(CONFIG_DATA.VALUES.category_max_price),
//         values: [parseFloat(CONFIG_DATA.VALUES.min_price), parseFloat(CONFIG_DATA.VALUES.max_price)],
//         step: 1,
//         slide: function (event, ui) {
//             $("#min-price").html(ui.values[0]);
//             $("#max-price").html(ui.values[1]);
//         },
//         change: function (event, ui) {
//             console.log('get_filtered_products()');
//             // update_url_filters();
//         }
//     });
// }

function update_attributes(first_time = false) {

    if ($('.filters-list').length <= 0) {
        return
    }
    let options_values = [];
    let options = [];
    for (let option of CONFIG_DATA.VALUES.ARRAY_OPTIONS) {
        for (let option_value of option.option_values) {
            if (option_value.checked === 1) {
                options_values.push({
                    'id': option_value.id,
                    'name': option_value.name,
                    'option_id': option_value.option_id,
                    'count_products': option_value.count_products,
                    'checked': 1,
                })
            }

        }
        if (options_values.length !== 0)
            options.push({
                'option': {
                    'id': option.option.id,
                    'name': option.option.name,
                },
                'option_values': options_values
            });
        options_values = [];
    }

    let attributes_values = [];
    let attributes = [];
    for (let attribute of CONFIG_DATA.VALUES.ARRAY_ATTRIBUTES) {
        for (let attribute_value of attribute.attribute_values) {
            if (attribute_value.checked === 1) {
                attributes_values.push({
                    'id': attribute_value.id,
                    'name': attribute_value.name,
                    'attribute_id': attribute_value.attribute_id,
                    'count_products': attribute_value.count_products,
                    'checked': 1,
                })
            }

        }
        if (attributes_values.length !== 0)
            attributes.push({
                'attribute': {
                    'id': attribute.attribute.id,
                    'name': attribute.attribute.name,
                },
                'attribute_values': attributes_values
            });
        attributes_values = [];
    }

    let content = {
        'category_pk': CONFIG_DATA.VALUES.category_id,
        'products': CONFIG_DATA.VALUES.ARRAY_PRODUCTS.length > 0 ? JSON.stringify(CONFIG_DATA.VALUES.ARRAY_PRODUCTS) : JSON.stringify(null),
        'attributes': attributes.length > 0 ? JSON.stringify(attributes) : JSON.stringify(null),
        'options': options.length > 0 ? JSON.stringify(options) : JSON.stringify(null),
        'min-price': parseFloat($("#min-price").html()),
        'max-price': parseFloat($("#max-price").html()),
        'page': 1,
        'sorting': $('#sorting :selected').val(),
    };
    if (typeof $('#search_input').val() !== 'undefined') {
        content.search_input = $('#search_input').val();
    }
    if ($(".attribute .filter-values.show").length > 0) {
        content.last_attribute_select = parseInt($(".attribute .filter-values.show").data('attr'));
    }
    if ($(".option .filter-values.show").length > 0) {
        content.last_option_select = parseInt($(".option .filter-values.show").data('option'));
    }

    $.ajax({
        type: "POST",
        data: content,
        url: CONFIG_DATA.URLS.get_template_catalog,
        success: function (data) {
            if (first_time) {
                let filter = $(".filters-list");
                filter.html(data.template_filters);
                $("#products").html(data.template_products);
            } else {
                let filter = $(".filters-list");
                filter.html(data.template_filters);
                $("#products").html(data.template_products);
            }
            build_price_track();
        }
    });
}

function get_template_products_cart(products_id, page = 1) {
    // Тестую вивод темплейта через запрос аякс
    let html = '';
    $.ajax({
        type: "POST",
        data: {
            'products_id': products_id,
            'page': page,
            'sorting': $('#sorting :selected').val(),
        },
        async: false,
        url: CONFIG_DATA.URLS.get_template_products_cart,
        success: function (data) {
            html += data;
        }
    });
    return html;
}

function refresh_array_attributes(attribute_id, attribute_value_id, filter_field) {
    for (let attribute of CONFIG_DATA.VALUES.ARRAY_ATTRIBUTES) {
        if (attribute.attribute.id === attribute_id) {
            for (let attribute_value of attribute.attribute_values) {
                if (attribute_value.id === attribute_value_id) {
                    if (filter_field.is(':checked') === true)
                        attribute_value.checked = 1;
                    else {
                        attribute_value.checked = 0;
                    }
                }
            }
        }
    }
}

function refresh_array_options(option_id, option_value_id, filter_field) {
    for (let option of CONFIG_DATA.VALUES.ARRAY_OPTIONS) {
        if (option.option.id === option_id) {
            for (let option_value of option.option_values) {
                if (option_value.id === option_value_id) {
                    if (filter_field.is(':checked') === true)
                        option_value.checked = 1;
                    else {
                        option_value.checked = 0;
                    }
                }
            }
        }
    }
}


body.on('click', '#language_toggle .language_item', function (e) {
    e.preventDefault();
    let btn = $(this);
    $.ajax({
        type: "POST",
        url: CONFIG_DATA.URLS.lang,

        data: {
            'next': btn.data('next'),
            'language': btn.data('code'),
            'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
        },
        success: function (data) {
            document.location.replace(data);
        },
    });
});

body.on('click', '#currency_toggle .currency_item', function (e) {
    e.preventDefault();
    let btn = $(this);
    $.ajax({
        type: "POST",
        url: CONFIG_DATA.URLS.currency_set,

        data: {
            'code': btn.data('code'),
            'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
        },
        success: function (data) {
            document.location.reload();
        },
    });
});


function ValidateEmail(email) {
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}

function searchToObject() {
    let pairs = window.location.search.substring(1).split("&"),
        obj = {},
        pair,
        i;

    for (i in pairs) {
        if (pairs[i] === "") continue;

        pair = pairs[i].split("=");
        obj[decodeURIComponent(pair[0])] = decodeURIComponent(pair[1]);
    }

    return obj;
}

function updateCurrentUrl(name_parameter, value_str) {
    let current_search_obj = searchToObject();
    let new_search_url = "?";
    let first_iteration = true;
    if (name_parameter in current_search_obj === false) {
        console.log('not_in');
        new_search_url += `${name_parameter}=${value_str}`;
        first_iteration = false;
    }

    for (let search_item in current_search_obj) {
        if (!first_iteration) {
            new_search_url += '&'
        }
        if (search_item === name_parameter) {
            new_search_url += search_item + "=" + value_str;
        } else {
            new_search_url += `${search_item}=${current_search_obj[search_item]}`;
        }
        first_iteration = false
    }
    let current_path = window.location.pathname;
    window.history.replaceState(null, null, current_path + new_search_url);
    return new_search_url;
}

function update_url_filters() {
    let min_price = parseFloat($('#min-price').text());
    let max_price = parseFloat($('#max-price').text());
    let filter_inputs_data = {
        min_price: Math.floor(parseFloat(convert_to_default(min_price))),
        max_price: Math.ceil(parseFloat(convert_to_default(max_price))),
        category_id: CONFIG_DATA.VALUES.category_id,
    };

    let inputs_attributes_checked = $(".filter-attr-wrapper.attribute [id^='attribute-value-'] input[id^='filter-attribute-']:checked");
    inputs_attributes_checked.each((key, value) => {
        if (!("attributes_id" in filter_inputs_data))
            filter_inputs_data['attributes_id'] = [];
        if (!("attributes_values_id" in filter_inputs_data))
            filter_inputs_data['attributes_values_id'] = [];
        let attr_id = parseInt(value.dataset.attr_id);
        let attr_value_id = parseInt(value.dataset.attr_value_id);
        if (filter_inputs_data.attributes_id.indexOf(attr_id) === -1) {
            filter_inputs_data.attributes_id.push(attr_id);
        }
        if (filter_inputs_data.attributes_values_id.indexOf(attr_value_id) === -1) {
            filter_inputs_data.attributes_values_id.push(attr_value_id);
        }
    });
    let inputs_filters_checked = $(".filter-attr-wrapper.filter [id^='filter-value-'] input[id^='filter-filter-']:checked");

    inputs_filters_checked.each((key, value) => {
        if (!("filters_id" in filter_inputs_data))
            filter_inputs_data['filters_id'] = [];
        if (!("filters_values_id" in filter_inputs_data))
            filter_inputs_data['filters_values_id'] = [];
        let filt_id = parseInt(value.dataset.filter_id);
        let filt_value_id = parseInt(value.dataset.filter_value_id);
        if (filter_inputs_data.filters_id.indexOf(filt_id) === -1) {
            filter_inputs_data.filters_id.push(filt_id);
        }
        if (filter_inputs_data.filters_values_id.indexOf(filt_value_id) === -1) {
            filter_inputs_data.filters_values_id.push(filt_value_id);
        }
    });
    let inputs_options_checked = $(".filter-attr-wrapper.option [id^='option-value-'] input[id^='filter-option-']:checked");
    inputs_options_checked.each((key, value) => {
        if (!("options_id" in filter_inputs_data))
            filter_inputs_data['options_id'] = [];
        if (!("options_values_id" in filter_inputs_data))
            filter_inputs_data['options_values_id'] = [];
        let option_id = parseInt(value.dataset.option_id);
        let option_value_id = parseInt(value.dataset.option_value_id);
        if (filter_inputs_data.options_id.indexOf(option_id) === -1) {
            filter_inputs_data.options_id.push(option_id);
        }
        if (filter_inputs_data.options_values_id.indexOf(option_value_id) === -1) {
            filter_inputs_data.options_values_id.push(option_value_id);
        }
    });
    updateCurrentUrl('filter_json', JSON.stringify(filter_inputs_data));
    if ($('input').is('#search_input')) {
        updateCurrentUrl('query', $('#search_input').val());
    }
    if ($('input').is('#category_id')) {
        updateCurrentUrl('category_id', $('#category_id').val());
    }

    let search_object = searchToObject();
    if ('page' in search_object) {
        filter_inputs_data.page = search_object.page;
    }
    if ('sorting' in search_object) {
        filter_inputs_data.sorting = search_object.sorting;
    }
    if ('query' in search_object) {
        filter_inputs_data.query = search_object.query;
    }
    if ('category_id' in search_object) {
        filter_inputs_data.category_id = search_object.category_id;
    }
    fetch(CONFIG_DATA.URLS.get_template_catalog, {
        method: 'POST', // or 'PUT'
        body: JSON.stringify(filter_inputs_data), // data can be `string` or {object}!
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json())
        .then((response) => {
            $('#products').html(response['products_template']);
            $('#js_category_badges').html(response['chips_template']);
            if ($('#js_category_badges > *').length > 0) {
                $('#js_active_filters_heading').show();
            } else {
                $('#js_active_filters_heading').hide();
            }
        }).catch(error => console.error('Error:', error));

    //window.location.reload();
    //Object.assign(CONFIG_DATA.VALUES, {categowry_id: category.object.pk });
}

$("#search_in_search_page_input").keydown(function (e) {
    if (e.keyCode === 13) {
        $('#search_in_search_page').focus().click()
    }
})

$('#load_more_wishlist').on('click', function (e) {
    let page = parseInt($('#wishlist_current_page').val());
    page += 1;
    $.ajax({
        type: "POST",
        data: {
            'page': page,
        },
        async: true,
        url: CONFIG_DATA.URLS.wishlist_load_more,
        success: function (data) {
            $('#wishlist_current_page').val(page);
            $('#paginator_block_wishlist').before(data.template);
            if (data.has_next_page === false) {
                $('#load_more_wishlist').css("visibility", "hidden");
            }
        }
    });
});

function del_from_wishlist(btn, content, product_id) {
    $.ajax({
        type: "POST",
        url: CONFIG_DATA.URLS.del_from_wishlist,
        data: content,
        success: function (data) {
            if (data.success) {
                btn.removeClass('active');
                $('.wishlist .item[data-id="' + product_id + '"]').stop().animate({
                        height: "0px",
                        paddingTop: "0px",
                        paddingBottom: "0px",
                        opacity: 0,
                    }, 400, function () {
                        $(this).remove();
                    }
                );
            }
        }
    });
}

function del_from_comparison(content) {
    let res = false;
    $.ajax({
        type: "POST",
        async: false,
        url: CONFIG_DATA.URLS.del_from_comparison,
        data: content,
        success: function (data) {
            res = data
        }
    });
    return res
}


function del_from_cart(content) {
    let res = null;
    $.ajax({
        type: "POST",
        async: false,
        url: CONFIG_DATA.URLS.remove_from_cart,
        data: content,
        success: function (data) {
            res = data;
        }
    });
    return res;
}

function initMap() {
    // The location of Uluru
    const uluru = {lat: 50.24478, lng: 30.32538};
    // The map, centered at Uluru
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 10,
        center: uluru,
    });
    // The marker, positioned at Uluru
    let marker = new google.maps.Marker({
        position: uluru,
        map: map,
    });
    $.ajax({
        type: "POST",
        async: false,
        url: CONFIG_DATA.URLS.api_google_map,
        success: function (data) {
            result = data;

        }
    });


    var markers = [];
    for (let info_marker in result.data) {
        markers.push([result.data[info_marker].name_marker, result.data[info_marker].lat, result.data[info_marker].longitude,])
    }
    for (i = 0; i < markers.length; i++) {
        var position = new google.maps.LatLng(markers[i][1], markers[i][2]);
        marker = new google.maps.Marker({
            position: position,
            map: map,
            title: markers[i][0],
        });
    }
}

function get_delivery_address() {
    let res = null;
    switch (DELIVERY_TYPE) {
        case 'self':
            break;
        case 'courier':
        case 'delivery':
        case 'ukr_post':
        case 'in_time':
        case 'avtoluks':
            res = {
                'delivery_obl': $('#custom_obl_input').val(),
                'delivery_settlement': $('#custom_settlement_input').val(),
                'delivery_street': $('#custom_street_input').val(),
                'delivery_house': $('#custom_house_input').val(),
            };
            break;
        case 'new_post':
            res = {
                'delivery_settlement': NP_SETTLEMENT,
                'delivery_street': NP_WAREHOUSE,
            };
            break;
    }
    return res;
}

//#endregion FUNCTIONS

//#region EVENTS
body.on('click', '.read-more', function (e) {
        $(this).toggleClass('expanded')
})

body.on('click', '#add-new-testimonial-button', function (e) {
    show_modal_testimonial()
})
body.on('click', '.close_form', function (e) {
    M.Modal.getInstance(document.getElementById('modal-testimonials')).close();
})
//CHECKOUT
body.on('click', '#left_menu_toggle', function (e) {
    $('#left_menu').toggleClass('opened');
});
body.on('click', '#collapse_search', function (e) {
    $('.top_header .quick_search_wrapper').toggleClass('collapsed');
});
body.on('click', '#mobile_menu_toggle', function (e) {
    $('#mobile_menu').toggleClass('active');
});
body.on('click', '#mobile_menu_close', (e) => {
    $('#mobile_menu').removeClass('active');
});
body.on('click', '#search_toggle', function (e) {
    e.preventDefault();
    $('.search_modal').show();
});
body.on('click', '#new_post_city_search_wrapper .dropdown-item', function (e) {
    let item = $(this);
    CITY_REF = item.attr('data-ref');
    CITY_NAME = item.attr('data-city');
    NP_SETTLEMENT = $(this).html();
    NP_WAREHOUSE = null;
    $('#new_post_city').html($(this).html());
    //$('#new_post_city_search_wrapper').hide();
    $('#new_post_city_input').val($(this).html());
    $('#new_post_city_search_wrapper .autocomplete-dropdown').remove();
    $('#new_post_warehouse').html(CONFIG_DATA.TRANS.not_selected);
    $('#new_post_warehouse_section').show();
});
body.on('click', '#new_post_warehouse_search_wrapper .dropdown-item', function (e) {
    NP_WAREHOUSE = $(this).html();
    //$('#new_post_warehouse').html($(this).html());
    //$('#new_post_warehouse_search_wrapper').hide();
    $('#new_post_warehouse_input').val($(this).html());
    $('#new_post_warehouse_search_wrapper .autocomplete-dropdown').remove();
});
body.on('click', '#other_delivery_settlement_search_wrapper .dropdown-item', function (e) {
    OD_SETTLEMENT = $(this).html();
    //$('#other_delivery_settlement').html($(this).html());
    //$('#other_delivery_settlement_search_wrapper').hide();
    $('#other_delivery_settlement_input').val($(this).html());
    $('#other_delivery_settlement_search_wrapper .autocomplete-dropdown').remove();
});

body.on('click', '.badges .value', function (e) {
    let t = $(this);

    if (t.hasClass('active')) {
        t.removeClass('active');
        let new_price = get_product_price_by_options($(this).attr('data-product-id'));
        $('.current_price').html(new_price.current_price);
        $('.stable_price').html(new_price.stable_price)
        return true
    }
    $(`.value[data-option-id=${t.attr('data-option-id')}][data-product-id=${t.attr('data-product-id')}]`).removeClass('active');
    t.addClass('active');

    let new_price = get_product_price_by_options($(this).attr('data-product-id'));
    $('.current_price').html(new_price.current_price);
    $('.stable_price').html(new_price.stable_price)

});

body.on('input', '.cart_item .item_qty', function (e) {
    let v = e.target.value;
    let item_id = $(this).attr('data-item-id');
    if (v === "") e.target.value = 0;
    $.ajax({
        type: 'POST',
        url: CONFIG_DATA.URLS.change_item_qty,
        data: {
            operation: JSON.stringify({name: 'assign', value: v}),
            item_id: item_id,
            csrfmiddlewaretoken: csrf,
        },
        success: function (data) {
            if (data.success) {
                refresh_total_qty(data.cart_items_count);
                refresh_total_price(data.cart_total_price)
                $('.cart_item[data-cart-item-id="' + item_id + '"]').replaceWith(data.cart_item_html);
                let new_input = document.querySelector(`.cart_items_checkout input.item_qty[data-item-id="${item_id}"]`);
                new_input.focus();
                new_input.selectionStart = new_input.value.length;
            }
        }
    })
});

body.on('click', '.qty_panel span', function (e) {
    let item_id = $(this).attr('data-item-id');
    let current_qty = $('.item_qty[data-item-id="' + item_id + '"]');
    let content = {};
    current_qty.addClass('loading');
    if ($(this).hasClass('plus')) {
        content = {
            operation: JSON.stringify({name: 'plus'}),
            item_id: item_id,
            csrfmiddlewaretoken: csrf,

        };
    }
    if ($(this).hasClass('minus')) {
        if (current_qty.val() - 1 <= 0) {
            return false;
        }
        content = {
            operation: JSON.stringify({name: 'minus'}),
            item_id: item_id,
            csrfmiddlewaretoken: csrf,
        };
    }
    $.ajax({
        type: 'POST',
        url: CONFIG_DATA.URLS.change_item_qty,
        data: content,
        success: function (data) {
            if (data.success == true) {
                refresh_total_qty(data.cart_items_count);
                refresh_total_price(data.cart_total_price)
                $('.cart_items_checkout .cart_item[data-cart-item-id="' + item_id + '"]').replaceWith(data.cart_item_html['checkout']);
                $('.cart_items_dropdown .cart_item[data-cart-item-id="' + item_id + '"]').replaceWith(data.cart_item_html['dropdown']);
            } else {
                swal("", data.message, "warning");
            }
            current_qty.removeClass('loading');

        }
    })
});


body.on('click', '.del_from_cart', function (e) {
    e.preventDefault();
    let cart_item_id = $(this).attr('data-cart-item-id');
    let content = {
        "cart_item_id": cart_item_id,
        "csrfmiddlewaretoken": csrf,
    };
    let res = del_from_cart(content);
    console.log(res);
    if (res.success) {
        refresh_total_qty(res.cart_items_count);
        refresh_total_price(res.cart_total_price)
        $('.cart_item[data-cart-item-id="' + cart_item_id + '"]').stop().animate({
                height: "0px",
                margin: "0px",
                paddingTop: "0px",
                paddingBottom: "0px",
                opacity: 0,
            }, 500, function () {
                $(this).remove();
            }
        );
    }
});

body.on('click', '#newsletter_submit', function (e) {
    let content = {
        'email': $('#newsletter_input').val()
    };
    $.ajax({
        type: "POST",
        url: CONFIG_DATA.URLS.newsletter_add_email,
        data: content,
        success: function (data) {
            console.log(data);
            if (data.success) {
                swal("", data.msg, "success");
                $('#newsletter_input').val('');
            } else {
                swal("", data.msg, "error");
            }
        }
    });
});

body.on('click', '.js-toggle-wishlist', function (e) {
    e.preventDefault();
    let content = {
        'product_id': $(this).attr('data-product-id'),
    };
    let btn = $(this);
    if (btn.hasClass('active')) {
        del_from_wishlist(btn, content, content.product_id);
    } else {
        $.ajax({
            type: "POST",
            url: CONFIG_DATA.URLS.add_to_wishlist,
            data: content,
            success: function (data) {
                if (data.success) {
                    btn.addClass('active');
                    //$('.alert span').html(CONFIG_DATA.TRANS.account__add_to_wishlist_success_response);
                    // let alert = $('.alert');
                    // alert.show('fade');
                    // setTimeout(function () {
                    //     alert.fadeOut(800);
                    // }, 4000)
                } else {
                    if (data.redirect) {
                        window.location.href = data.redirect;
                    }
                }
            }
        });
    }

});
body.on('click', '.del_from_wishlist', function (e) {
    e.preventDefault();
    let product_id = $(this).attr('data-product-id');
    let content = {
        'product_id': product_id,
    };
    del_from_wishlist($(this), content, product_id);
});
body.on('click', '.add_to_comparison', function (e) {
    e.preventDefault();
    let t = $(this);
    let content = {
        'product_id': $(this).attr('data-product-id'),
    };
    if (t.hasClass('active')) {
        let res = del_from_comparison(content);
        if (res.success) {
            $(this).removeClass('active');
        }
    } else {
        $.ajax({
            type: "POST",
            url: CONFIG_DATA.URLS.add_to_comparison,
            data: content,
            success: function (data) {
                console.log(t);
                if (data.success) {
                    t.addClass('active');
                }
            }
        });
    }
});
body.on('click', '.del-from-comparison', function (e) {
    let content = {
        'product_id': $(this).attr('data-product-id'),
    };
    let res = del_from_comparison(content);
    if (res.success) {
        $(this).removeClass('active');
    }
    document.location.reload()
});
body.on('click', '.del-from-comparison-page', function (e) {
    let content = {
        'product_id': $(this).attr('data-product-id'),
    };
    let res = del_from_comparison(content);
    if (res.success) {
        location.reload();
    }
});

body.on('click', '.js-quick-order', function (e) {
    e.preventDefault();
    let product_id = $(this).attr('data-product-id');
    let options = JSON.stringify(get_selected_options(product_id, 'badges'));
    let content = {
        "product_id": product_id,
        "options": options,
        "csrfmiddlewaretoken": csrf,
    };
    M.Modal.getInstance(document.getElementById('quick_order_modal')).open();
    //let required = $('.option.js-required .values_wrapper .value.active').length < $('.option.js-required').length;

    // $.ajax({
    //     type: "POST",
    //     url: CONFIG_DATA.URLS.render_quick_order_item,
    //     data: content,
    //     success: function (data) {
    //         if (data.success === false && data.error === 'no_required') {
    //
    //             $.each(data.required, function (key, value) {
    //                 let temp = $('.option-title[data-product-id="' + product_id + '"][data-option-id="' + value + '"]');
    //                 temp.addClass('required-s');
    //                 setTimeout(function () {
    //                     temp.removeClass('required-s');
    //                 }, 2000);
    //             });
    //         } else {
    //             $('#quick_order_modal #quick_order_item').html(data['html']);
    //             M.Modal.getInstance(document.getElementById('quick_order_modal')).open();
    //
    //         }
    //     }
    // });
});
body.on('click', '#js-quick-order-submit', function (e) {
    let product_id = $(this).attr('data-product-id');
    let content = {
        product_id: product_id,
        phone: $('.js-phone-input').val(),
        first_name: $('.js-name-input').val(),
        product_options: [],
        csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()
    };
    content.product_options = get_selected_options(product_id, 'badges');

    $.ajax({
        type: "POST",

        url: CONFIG_DATA.URLS.add_one_click_order,
        data: content,
        success: function (data) {
            if (data.success === true) {
                swal("", data.message, "success").then(() => {
                    M.Modal.getInstance(document.getElementById('quick_order_modal')).close();
                });
                $('.buy_in_one_click_modal').hide();

            } else {
                swal("", data.message, "error");
            }
        }
    });

});

body.on('click', 'a.filter-attr', function (e) {
    let dropdown_id = $(e.target).data('attr-index');
    if (typeof dropdown_id !== 'undefined') {
        let dropdown = $("[data-attr='" + dropdown_id + "']");
        if (dropdown.hasClass('show')) {
            $('.filter-values').removeClass('show');
            dropdown.removeClass('show');
        } else {
            $('.filter-values').removeClass('show');
            dropdown.addClass('show');
        }
    }

    let dropdown_id_filter = $(e.target).data('filter-index');
    if (typeof dropdown_id_filter !== 'undefined') {
        let dropdown_filter = $("[data-filter='" + dropdown_id_filter + "']");
        if (dropdown_filter.hasClass('show')) {
            $('.filter-values').removeClass('show');
            dropdown_filter.removeClass('show');
        } else {
            $('.filter-values').removeClass('show');
            dropdown_filter.addClass('show');
        }
    }

    let dropdown_id_option = $(e.target).data('option-index');
    if (typeof dropdown_id_option !== 'undefined') {
        let dropdown_option = $("[data-option='" + dropdown_id_option + "']");
        if (dropdown_option.hasClass('show')) {
            $('.filter-values').removeClass('show');
            dropdown_option.removeClass('show');
        } else {
            $('.filter-values').removeClass('show');
            dropdown_option.addClass('show');
        }
    }
});
// body.on('change', '.filter-input-value', function (e) {
//     let filter_field = $(this);
//     let attribute_id = filter_field.data('attr_id');
//     let attribute_value_id = filter_field.data('attr_value_id');
//     refresh_array_attributes(attribute_id, attribute_value_id, filter_field);
//     update_attributes();
// });
// body.on('change', '.filter-option-input-value', function (e) {
//     let filter_field = $(this);
//     let option_id = filter_field.data('option_id');
//     let option_value_id = filter_field.data('option_value_id');
//     refresh_array_options(option_id, option_value_id, filter_field);
//     update_attributes();
// });
body.on('change', 'input[name="sorting"]', function (e) {
    console.log("sord");
    updateCurrentUrl('sorting', $('input[name="sorting"]:checked').val());
    update_url_filters();
});
body.on('click', "div[id=products] .page_item a", function (e) { /* Подія для пагінації */
    e.preventDefault();
    let page = this.getAttribute('href').match(/page=([0-9]+)/i);
    console.log(page[1]);
    updateCurrentUrl('page', page[1]);
    update_url_filters();
});
body.on('click', '.page-load-next', function (e) {
    e.preventDefault();
    if (this.getAttribute('href').search('api') !== -1) {
        let page = this.getAttribute('href').match(/page=([0-9]+)/i);
        let pagination_block = $('.pagination-block');
        let page_load_nex = $('.page-load-next');
        for (let block of pagination_block) {
            $(block).remove();
        }
        for (let page_next of page_load_nex) {
            $(page_next).remove();
        }
        $("#products").append(get_template_products_cart(CONFIG_DATA.VALUES.ARRAY_PRODUCTS_FILTERED, page[1]));
    } else {
        let page = this.getAttribute('href').match(/page=([0-9]+)/i);
        let URL = '';
        if (document.location.href.search('page=') !== -1) {
            URL = document.location.href + ',' + page[1];
        } else {
            URL = document.location.href + '?sorting=' + $('#sorting :selected').val() + '&page=1,' + page[1];
        }
        document.location.href = URL.replace('#page_load_next', '') + "#page_load_next";
    }
});

body.on('click', '#feedback_form_button', function (e) {
    M.Modal.getInstance(document.getElementById('feedback_form_modal')).open();
});

body.on('click', '#feedback_form_modal #submit_form', function (e) {
    $("div.error-message").remove();
    let btn = $(this);
    e.preventDefault();
    if (!btn.hasClass('loading')) {
        btn.addClass('loading');
        let content = {
            name: $('#ff_name').val(),
            country: $('#ff_country').val(),
            cooperation: $('#ff_cooperation').val(),
            phone: $('#ff_phone').val(),
            email: $('#ff_email').val(),
            comment: $('#ff_comment').val(),
        };
        $.ajax({
            type: "POST",
            url: CONFIG_DATA.URLS.feedback_form__add_message,
            data: content,
            success: function (data) {
                btn.removeClass('loading');
                if (data.success) {
                    $('#feedback_form_modal input, #feedback_form_modal textarea').val('');
                    swal({
                        icon: 'success',
                        className: 'custom_swal',
                        text: data.message,
                    }).then(() => {
                        M.Modal.getInstance(document.getElementById('feedback_form_modal')).close();
                    });
                } else {
                    if (data.message) {
                        swal({
                            icon: 'error',
                            className: 'custom_swal',
                            text: data.message
                        });
                    } else {
                        for (let error of data['error']) {
                            for (let key in error) {
                                let field = $(key);
                                field.after("<div class='text-danger error-message'>" + error[key] + "</div>");
                            }
                        }
                    }
                }
            }
        });
    }
});
body.on('click', '.repay-order', function (e) {
    e.preventDefault();
    let order_id = $(this).attr('data-order-id');
    let csrf = $('[name="csrfmiddlewaretoken"]').val();
    console.log(order_id);
    let content = {
        "order_id": order_id,
        'csrfmiddlewaretoken': csrf
    };

    $.ajax({
        type: "POST",
        url: CONFIG_DATA.URLS.repay,
        data: content,
        success: function (data) {
            window.open(data.redirect);
        }
    })
});
body.on('click', '.list .order', function (e) {
    let order_id = $(this).attr('data-id');
    let csrf = $('[name="csrfmiddlewaretoken"]').val();

    let content = {
        "order_id": order_id,
        'csrfmiddlewaretoken': csrf
    };

    $.ajax({
        type: "POST",
        url: CONFIG_DATA.URLS.get_order_detail,
        data: content,
        success: function (data) {
            console.log(data);
            if (data.success) {
                $('.right-col').html(data.html);
            }

        }
    })
});

body.on('click', '.nwa-btn', function (e) {
    let product_id = $(this).attr('data-product-id');
    let content = {
        'product_id': product_id,
        'product_options': []
    };
    content.product_options = JSON.stringify(get_selected_options(product_id));
    $.ajax({
        url: CONFIG_DATA.URLS.render_notify_when_available,
        type: 'POST',
        data: content,
        success: function (data) {
            console.log(data);
            $('#nwa-modal').html(data.html);
            $('#nwa-modal').modal();
        }
    })
});
body.on('click', '#nwa-submit', function (e) {
    let email = $('#nwa-email').val();
    console.log(email);
    if (ValidateEmail(email) === false) {
        console.log("error");
        return false;
    }

    let product_id = $(this).attr('data-product-id');

    let content = {
        "product_id": product_id,
        "email": email,
    };

    $.ajax({
        type: "POST",
        url: CONFIG_DATA.URLS.add_notify,
        data: content,
        success: function (data) {
            if (data.success === true) {
                swal("", CONFIG_DATA.TRANS.OneClickOrder_SuccessMessage, "success");
                $('#nwa-modal').modal('toggle');
            } else {

            }
        }
    });

});
body.on('click', ".filter-attr-wrapper.attribute [id^='attribute-value-'] input[id^='filter-attribute'],.filter-attr-wrapper.option [id^='option-value-'] input[id^='filter-option-'],.filter-attr-wrapper.filter [id^='filter-value-'] input[id^='filter-filter-']", function (e) {
    update_url_filters();
});
body.on('click', ".js_chip_filter_update", function (e) {
    let filter = $(e.target)
    // console.log(`.filter-attr-wrapper.${filter.data('type')} #filter-${filter.data('id')}-${filter.data('id_v')}`)
    $(`.filter-attr-wrapper.${filter.data('type')} #filter-${filter.data('type')}-${filter.data('id')}-${filter.data('id_v')}`).prop("checked", false);
    update_url_filters();
})
body.on('input', '#search_query', function (e) {
    let inp = $(this);
    if (inp.val().length < 1) {
        $('#search_results').html('');
        return false;
    }
    if (inp.val().length < 3) {
        return
    }
    let query = inp.val();
    //$('#search_results').html('<img class="loading" src="/media/icons/loading.gif">');
    $.ajax({
        type: "POST",
        url: CONFIG_DATA.URLS.search_product_by_query,
        data: {
            'q': query,
            'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
        },
        success: function (data) {
            $('#search_results').html(data.html);
        },
    });
});
body.on('click', '.reset-filter', function (e) {
    e.preventDefault();
    document.location.href = document.location.origin + document.location.pathname;
});

body.on('click', '.search_submit', function (e) {
    let search_by_query = $('#search_query').val();
    window.location.href = CONFIG_DATA.URLS.search + '?query=' + search_by_query;
});

body.on('click', '.order-history .item .collapse', function (e) {
    e.preventDefault();
    let id = $(this).attr('data-id');
    console.log(id);
    let row = $('.order-history .item[data-id="' + id + '"]');
    row.toggleClass('opened');
});
body.on('click', '#menu li > a[class="next"] > span', function (e) {
    window.location.href = $(this).parent().attr('href')
});
body.on('click', '#new_post_city_search_wrapper .dropdown-item', function (e) {
    let item = $(this);
    CITY_REF = item.attr('data-ref');
    CITY_NAME = item.attr('data-city');
    NP_SETTLEMENT = $(this).html();
    NP_WAREHOUSE = null;
    $('#new_post_city').html($(this).html());
    $('#new_post_city_search_wrapper').hide();
    $('#new_post_city_input').val('');
    $('#new_post_city_search_wrapper .autocomplete-dropdown').remove();
    $('#new_post_warehouse').html(CONFIG_DATA.TRANS.not_selected);
    $('#new_post_warehouse_section').show();
});
body.on('click', '#new_post_warehouse_search_wrapper .dropdown-item', function (e) {
    $('#new_post_warehouse').html($(this).html());
    NP_WAREHOUSE = $(this).html();
    $('#new_post_warehouse_search_wrapper').hide();
    $('#new_post_warehouse_input').val('');
    $('#new_post_warehouse_search_wrapper .autocomplete-dropdown').remove();
});
body.on('click', '#other_delivery_settlement_search_wrapper .dropdown-item', function (e) {
    OD_SETTLEMENT = $(this).html();
    $('#other_delivery_settlement').html($(this).html());
    $('#other_delivery_settlement_search_wrapper').hide();
    $('#other_delivery_settlement_input').val('');
    $('#other_delivery_settlement_search_wrapper .autocomplete-dropdown').remove();
});
body.on('change', '#similar-product', function (e) {
    window.location.href = e.target.value
});
body.on('click', '#search_in_search_page', function (e) {
    e.preventDefault();
    updateCurrentUrl('query', document.getElementById('search_in_search_page_input').value);
    update_url_filters();
});

lng_changer.on('change', function (e) {
    lng_form.submit();
});

$('.star-rating input').on('click', function (e) {
    $('.star-rating input').removeClass('active');
    for (let i = 0; i <= $(this).val(); i++) {
        $('.star-rating input[value="' + i + '"]').addClass('active');
    }
});
$('.main_carousel').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: false,
    fade: true,
    asNavFor: '.secondary_carousel',
    infinite: false,
});
$('.secondary_carousel').slick({
    slidesToShow: 3,
    adaptiveHeight: true,
    slidesToScroll: 1,
    asNavFor: '.main_carousel',
    focusOnSelect: true,
    arrows: true,
    prevArrow: '<button class="slick-prev" aria-label="Previous" type="button"><i class="material-icons arrow_color">arrow_back</i></button>',
    nextArrow: '<button class="slick-next" aria-label="Next" type="button"><i class="material-icons arrow_color">arrow_forward</i></button>',
});

$('.product-photos2').slick({
    infinite: false,
    speed: 300,
    slidesToShow: 2,
    slidesToScroll: 1,
    adaptiveHeight: true,
    variableWidth: true,
    prevArrow: '<button class="slick-prev" aria-label="Previous" type="button">Previous</button>',
    nextArrow: '<button class="slick-next" aria-label="Next" type="button">Next</button>',
    responsive: [
        {
            breakpoint: 768,
            settings: {
                slidesToShow: 1,
                slidesToScroll: 1,
            }
        }
    ]
});
$('#js-load-more-reviews').on('click', function (e) {
    let content = {
        'page': $(this).attr('data-page'),
        'product_id': $(this).attr('data-product-id'),
    };
    $.ajax({
        type: "POST",
        url: CONFIG_DATA.URLS.load_more_reviews,
        data: content,
        success: function (data) {
            console.log(data);
            if (data.success === true) {
                $('.js-product-reviews-list').append(data.html);

                if (data.next_page !== -1) {
                    $('#js-load-more-reviews').attr('data-page', data.next_page);
                } else {
                    $('#js-load-more-reviews').remove();
                }
            } else {

            }
        },
    });
});
$('#js-product-review-submit').on('click', function (e) {
    e.preventDefault();
    let content = {
        'author': $('#js-review-author').val(),
        'text': $('#js-review-text').val(),
        'rating': $('.rating-area input:checked').val(),
        'product_id': $(this).attr('data-product-id'),
    };
    console.log(content.rating)
    $.ajax({
        type: "POST",
        url: CONFIG_DATA.URLS.add_review,
        data: content,
        success: function (data) {
            if (data.success) {
                $('#js-review-author').val('');
                $('.rating-area input:checked').prop("checked", false);
                $('#js-review-text').val('');
                swal({
                    icon: 'success',
                    className: 'custom_swal',
                    text: data.message
                }).then(() => {
                    M.Modal.getInstance(document.getElementById('product_review_modal')).close();
                });
            } else {
                swal({
                    icon: 'error',
                    className: 'custom_swal',
                    text: data.message
                });
            }
        },
    });
});
$('.option-values').change(function (e) {
    let new_price = get_product_price_by_options($(this).attr('data-product-id'));
    let old_price = $('.new-price');
    if (new_price !== old_price) {
        if (new_price.discount !== 0) {
            $('.old-price').html(new_price.stable_price);
            $('.new-price').html(new_price.current_price)
            // $('.old-price').spincrement({
            //     to: parseFloat(new_price.stable_price),
            //     from: parseFloat($('.old-price').html()),
            //     duration: 200,
            //     decimalPlaces: 2,
            //     thousandSeparator: '',
            //     decimalPoint: '.'
            // });
        }
        // old_price.spincrement({
        //     to: parseFloat(new_price.current_price),
        //     from: parseFloat(old_price.html()),
        //     duration: 200,
        //     decimalPlaces: 2,
        //     thousandSeparator: '',
        //     decimalPoint: '.'
        // });
    }
});
// $('.options a.option-value').on('click', function (e) {
//     e.preventDefault();
//     mark_selected(e.target);
//
//     let new_price = get_product_price_by_options($(this).attr('data-product-id'));
//     let old_price = $('.new-price');
//
//     // old_price.spincrement({
//     //     to: convert_to_currency(parseFloat(new_price)),
//     //     from: old_price.html(),
//     //     duration: 200,
//     //     decimalPlaces: 2,
//     //     thousandSeparator: '',
//     //     decimalPoint: '.'
//     // });
// });
// function initialize_carousels() {
//     let carousels = $('.products_carousel');
//     carousels.each(function (i, key) {
//         let wrapper = $(key).find('.products_wrapper');
//         let show = wrapper.attr('data-show');
//         let items_count = wrapper.children('.product_item').length;
//         console.log(items_count);
//         if (show < items_count) {
//             wrapper.slick({
//                 infinite: true,
//                 slidesToScroll: parseInt(show),
//                 prevArrow: $(key).find('.navigation .prev'),
//                 nextArrow: $(key).find('.navigation .next'),
//                 responsive: [
//                     {
//                         breakpoint: 1200,
//                         settings: {
//                             slidesToShow: 3,
//                         }
//                     },
//                     {
//                         breakpoint: 992,
//                         settings: {
//                             slidesToShow: 3,
//                         }
//                     },
//                     {
//                         breakpoint: 768,
//                         settings: {
//                             slidesToShow: 2,
//
//                         }
//                     },
//                     {
//                         breakpoint: 576,
//                         settings: {
//                             slidesToShow: 1,
//                         }
//                     }
//                 ],
//                 slidesToShow: show,
//             })
//         }
//     });
// }
$('.products_carousel .products_wrapper').slick({
    slidesToShow: 4,
    slidesToScroll: 4,
    responsive: [
        {
            breakpoint: 1200,
            settings: {
                slidesToShow: 3,
                slidesToScroll: 3,
            }
        },
        {
            breakpoint: 992,
            settings: {
                slidesToShow: 2,
                slidesToScroll: 2,
            }
        },
        {
            breakpoint: 768,
            settings: {
                slidesToShow: 2,
                slidesToScroll: 2,

            }
        },
        {
            breakpoint: 576,
            settings: {
                slidesToShow: 1,
                slidesToScroll: 1,
            }
        }
    ],
});
$('#search-by-query').on('click', function (e) {
    e.preventDefault();
    let query = $('#search').val();
    location.href = CONFIG_DATA.URLS.search + '?query=' + query;
});

$('#newsletter-subscribe').on('click', function () {
    let mail = $('#subscribe_mail').val();
    if (ValidateEmail(mail)) {
        $.ajax({
            type: "POST",
            url: CONFIG_DATA.URLS.newsletter_add_email,
            data: {'mail': mail, 'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()},
            success: function (data) {
                console.log(data);
                if (data.success === true) {
                    swal("", "{% trans 'newsletter__success' %}", "success");
                    $('#subscribe_mail').val('');
                } else {
                    swal("", "{% trans 'newsletter__already_exists' %}", "error");
                    console.log(data.error);
                }
            },
        });
    } else {
        swal("", "{% trans 'newsletter__error' %}", "error");
    }
});


$("#password_reset").on('click', function (e) {
    let btn = $(this);
    if (!btn.hasClass('loading')) {
        e.preventDefault();
        btn.addClass('loading');
        $.ajax({
            url: CONFIG_DATA.URLS.account_password_reset,
            type: "POST",
            data: {
                'email': $('#email').val(),
                'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
            },
            success: function (data) {
                btn.removeClass('loading');

                if (data.success) {
                    swal({
                        icon: 'success',
                        className: 'custom_swal',
                        text: data.message
                    })
                } else {
                    swal({
                        title: "",
                        text: data.message,
                        icon: "error",
                        button: CONFIG_DATA.TRANS.Ok,
                    }).then(() => {

                    });
                }

            }
        })
    }
});
$('#difference').on('change', function (e) {
    let attrs = $('.attribute');
    attrs.each(function (key, value) {
        let attr_id = value.getAttribute('data-attr-id');
        let values = $('.product-value[data-attr-id=' + attr_id + ']');
        let res = values.map(function (idx, ele) {
            return $(ele).data('attr-val-id');
        }).get();

        console.log(res);
        if (new Set(res).size === 1) {
            console.log(value + ' одинакові');
            $("[data-attr-id='" + attr_id + "']").toggle();
        } else {
            console.log(value + ' НЕ одинакові');
        }
    });
});

$('#delivery_type').on('change', function (e) {
    $('.address-wrapper').hide();
    DELIVERY_TYPE = $(e.target).val();
    switch (DELIVERY_TYPE) {
        case 'delivery':
        case 'avtoluks':
        case 'ukr_post':
        case 'courier':
        case 'in_time':
            // case 'pickup':
            //     $('#custom_address').hide();
            //             $('#np_address').hide();
            //     break;
            $('#custom_address').show();
            $('#np_address').hide();
            break;
        case 'new_post':
            $('#custom_address').hide();
            $('#np_address').show();
            break;
        default:
            $('#custom_address').hide();
            $('#np_address').hide();

    }


    // if ($(this).val() === 'delivery') {
    //     $('#delivery-city').show();
    //     $('#delivery-warehouse').show();
    // }
    // if (($(this).val() === 'self')) {
    //     $('#delivery-city').hide();
    //     $('#delivery-warehouse').hide();
});
$('#liqpay_modal').on('hide.bs.modal', function (e) {
    document.location.href = CONFIG_DATA.URLS.index;
});

// $('#other_delivery_settlement_input').on("input", function (e) {
//     if ($(this).val() === '') {
//         $('.autocomplete-dropdown').remove();
//         return false;
//     }
//
//     let data = {
//         'query': $(this).val(),
//     };
//
//     $.ajax({
//         url: CONFIG_DATA.URLS.delivery__get_settlements,
//         type: "POST",
//         data: data,
//         success: function (response) {
//             $('.autocomplete-dropdown').remove();
//             $('#other_delivery_settlement_search_wrapper').append(response.html);
//         }
//     });
// });

// $('#new_post #new_post_city_input').on("input", function (e) {
//     if ($(this).val().length >= 2) {
//         if ($(this).val() === '') {
//             $('.autocomplete-dropdown').remove();
//             return false;
//         }
//
//         let data = {
//             'query': $(this).val(),
//         };
//
//         $.ajax({
//             url: CONFIG_DATA.URLS.np_get_cities,
//             type: "POST",
//             data: data,
//             success: function (response) {
//                 $('.autocomplete-dropdown').remove();
//                 $('#new_post_city_search_wrapper').append(response.html);
//             }
//         });
//     }
// });

// $('#new_post #new_post_warehouse_input').on("input", function (e) {
//     if (NP_SETTLEMENT === null) {
//         return false;
//     }
//     if ($(this).val() === '') {
//         $('.autocomplete-dropdown').remove();
//         return false;
//     }
//
//     let data = {
//         'query': $(this).val(),
//         'ref': CITY_REF,
//         'city': CITY_NAME,
//     };
//
//     $.ajax({
//         url: CONFIG_DATA.URLS.np_get_warehouses,
//         type: "POST",
//         data: data,
//         success: function (response) {
//             console.log(response);
//             $('.autocomplete-dropdown').remove();
//             $('#new_post #new_post_warehouse_search_wrapper').append(response.html);
//         }
//     });
// });

$('#np_settlement_input').on("input", function (e) {
    if ($(this).val().length >= 2) {
        if ($(this).val() === '') {
            $('.autocomplete-dropdown').remove();
            return false;
        }

        let data = {
            "query": $(this).val(),
            "csrfmiddlewaretoken": csrf,
        };

        $.ajax({
            url: CONFIG_DATA.URLS.np_get_cities,
            type: "POST",
            data: data,
            success: function (response) {
                $('.autocomplete-dropdown').remove();
                $('#np_settlement_wrapper').append(response.html);
            }
        });
    }
});

$('#np_warehouse_input').on("input", function (e) {
    if (NP_SETTLEMENT === null) {
        return false;
    }
    if ($(this).val() === '') {
        $('.autocomplete-dropdown').remove();
        return false;
    }
    let data = {
        'query': $(this).val(),
        'ref': CITY_REF,
        'city': CITY_NAME,
    };
    $.ajax({
        url: CONFIG_DATA.URLS.np_get_warehouses,
        type: "POST",
        data: data,
        success: function (response) {
            console.log(response);
            $('.autocomplete-dropdown').remove();
            $('#np_warehouse_wrapper').append(response.html);
        }
    });
});
body.on('click', '#np_settlement_wrapper .dropdown-item', function (e) {
    let item = $(this);
    CITY_REF = item.attr('data-ref');
    CITY_NAME = item.attr('data-city');
    NP_SETTLEMENT = $(this).html();
    NP_WAREHOUSE = null;
    $('#np_settlement_input').val($(this).html());
    $('.autocomplete-dropdown').remove();
});
body.on('click', '#np_warehouse_wrapper .dropdown-item', function (e) {
    NP_WAREHOUSE = $(this).html();
    $('#np_warehouse_input').val($(this).html());
    $('.autocomplete-dropdown').remove();
});

body.on('click', '#registration_submit', function (e) {
    $('.error_message').remove();
    let btn = $(this);
    if (btn.hasClass('loading')) {
        return false;
    }
    btn.addClass('loading');
    let data = {
        'csrfmiddlewaretoken': csrf,
        'first_name': $('#first_name').val(),
        'last_name': $('#last_name').val(),
        'phone': $('#phone').val(),
        'email': $('#email').val(),
        'password': $('#password').val(),
        're_password': $('#re_password').val(),
        'account_type': $("#account_type option:selected").val(),
    };
    $.ajax({
        url: CONFIG_DATA.URLS.view__registration,
        type: "POST",
        data: data,
        success: function (response) {
            if (response.success)
                swal({
                    text: data.message,
                    icon: "success",
                    className: 'custom_swal',
                }).then(() => {
                    window.location.href = CONFIG_DATA.URLS.view__login
                });
            else {
                console.log(response);
                $('#password').val('');
                $('#re_password').val('');
                for (let error of response['errors']) {
                    for (let key in error) {
                        let field = $(key);
                        field.after("<div class='error_message'>" + error[key] + "</div>");
                    }
                }
            }
            btn.removeClass('loading');
        }
    });
    return false;
});

body.on('click', '#login_submit', function (e) {
    $('.error_message').remove();
    let btn = $(this);
    if (btn.hasClass('loading')) {
        return false;
    }
    btn.addClass('loading');
    let data = {
        'csrfmiddlewaretoken': csrf,
        'username': $('#email').val(),
        'password': $('#password').val(),
    };
    $.ajax({
        url: CONFIG_DATA.URLS.view__login,
        type: "POST",
        data: data,
        success: function (response) {
            if (response.success) {
                window.location.href = response.redirect;
            } else {
                $('#password').val('');
                for (let error of response['errors']) {
                    for (let key in error) {
                        let field = $(key);
                        field.after("<div class='error_message'>" + error[key] + "</div>");
                    }
                }
            }
            btn.removeClass('loading');
        }
    });
    return false;
});

body.on('click', '#edit_account_submit', function (e) {
    $('.error_message').remove();
    let btn = $(this);
    if (btn.hasClass('loading')) {
        return false;
    }
    btn.addClass('loading');
    let data = {
        'csrfmiddlewaretoken': csrf,
        'email': $('#email').val(),
        'first_name': $('#first_name').val(),
        'last_name': $('#last_name').val(),
        'phone': $('#phone').val(),
        'account_type': $("#account_type option:selected").val(),
        'current_password': $('#current_password').val(),
        'new_password': $('#new_password').val(),
        're_password': $('#re_password').val(),

    };
    $.ajax({
        url: CONFIG_DATA.URLS.view__edit_profile,
        type: "POST",
        data: data,
        success: function (response) {
            if (response.success) {
                swal({
                    text: 'qwe',
                    icon: "success",
                    className: 'custom_swal',
                })
                document.location.reload();
            } else {
                $('#current_password').val('');
                //$('#new_password').val('');
                //$('#re_password').val('');
                for (let error of response['errors']) {
                    for (let key in error) {
                        let field = $(key);
                        field.after("<div class='error_message'>" + error[key] + "</div>");
                    }
                }
            }
            btn.removeClass('loading');
        }
    });

    return false;
});

$("#checkout_submit").on('click', function (e) {
    let btn = $(this);
    btn.addClass('loading');
    e.preventDefault();
    $('.error_message').remove();

    let content = {
        'csrfmiddlewaretoken': csrf,
        'first_name': $('#first_name').val(),
        'last_name': $('#last_name').val(),
        'email': $('#email').val(),
        'phone': $('#phone').val(),
        'payment_type': $('#payment_type option:selected').val(),
        'delivery_type': $('#delivery_type option:selected').val(),
        'comment': $("#comment").val(),
        'privacy_policy': $('#privacy_policy').is(':checked'),
    };

    let delivery_address = get_delivery_address();
    Object.assign(content, delivery_address);
    $.ajax({
        type: "POST",
        url: CONFIG_DATA.URLS.view__checkout,
        data: content,
        success: function (data) {
            if (data.success) {
                if (data.payment === true) {
                    $('#liqpay_modal .modal-body').append(data.button);
                    $('.modal').modal({dismissible: false});
                    M.Modal.getInstance(document.getElementById('liqpay_modal')).open()
                    //document.location.href = CONFIG_DATA.URLS.add_order_success_liqPay;
                } else {

                    swal({
                        className: 'custom_swal',
                        text: CONFIG_DATA.TRANS.checkout__success_message,
                    }).then(() => {
                        document.location.href = data.redirect;
                    });
                }
            } else {
                if (data.message) {
                    swal({
                        icon: 'info',
                        className: 'custom_swal',
                        text: data.message,
                    })
                }
                if (data.errors) {
                    for (let error of data['errors']) {
                        for (let key in error) {
                            let field = $(key);
                            field.after("<div class='error_message'>" + error[key] + "</div>");
                        }
                    }
                }
            }
            btn.removeClass('loading');
        }
    });
});

$('.page__login .input_v1').keypress(function (e) {
    if (e.which === 13) {
        jQuery('#login_submit').focus().click();
    }
});

$('.page__registration .input_v1').keypress(function (e) {
    if (e.which === 13) {
        jQuery('#registration_submit').focus().click();
    }
});

//#region Закріплення меню
// $('.main_nav').addClass('original').clone().insertAfter('.main_nav').addClass('cloned').css('position', 'fixed').css('top', '0').css('margin-top', '0').css('z-index', '500').removeClass('original').hide();
//
// scrollIntervalID = setInterval(stickIt, 10);
//
//
// function stickIt() {
//
//     var orgElementPos = $('.original').offset();
//     orgElementTop = orgElementPos.top;
//
//     if ($(window).scrollTop() >= (orgElementTop)) {
//         // scrolled past the original position; now only show the cloned, sticky element.
//
//         // Cloned element should always have same left position and width as original element.
//         orgElement = $('.original');
//         coordsOrgElement = orgElement.offset();
//         leftOrgElement = coordsOrgElement.left;
//         widthOrgElement = orgElement.css('width');
//         $('.cloned').css('left', leftOrgElement + 'px').css('top', 0).css('width', widthOrgElement).show();
//         $('.original').css('visibility', 'hidden');
//     } else {
//         // not scrolled past the menu; only show the original menu.
//         $('.cloned').hide();
//         $('.original').css('visibility', 'visible');
//     }
// }
//#endregion Закріплення меню



//#endregion EVENTS

//#region CHECKOUT
body.on('click', '.product_min .js_add_to_cart', async function (e) {
    e.preventDefault();
    let product_id = $(this).attr('data-product-id');
    let content = {
        "product_id": product_id,
        "product_options": [],
        "csrfmiddlewaretoken": csrf,
    };
    let res = await add_to_cart(content);
    if (res.required != null) {
        window.location.href = $(this).attr('data-url');
    }
});

body.on('click', '.product_info .js-add-to-cart', async function (e) {
    e.preventDefault();
    if ($(this).hasClass('loading')) return;
    $(this).addClass('loading');
    let product_id = $(this).attr('data-product-id');
    //let qty = $(`.add_to_cart_qty[data-product-id="${product_id}"]`).val();
    let content = {
        "product_id": product_id,
        "qty": 1,
        "product_options": [],
        "csrfmiddlewaretoken": csrf,
    };
    content.product_options = JSON.stringify(get_selected_options(product_id, 'badges'));

    let res = await add_to_cart(content);
    if (res.required) {
        swal({
            icon: 'info',
            className: 'custom_swal',
            text: res.message,
        })
    }
    /*
    if (res && res.required) {
        $.each(res.required, function (key, value) {
            let temp = $('.option-title[data-product-id="' + product_id + '"][data-option-id="' + value + '"]');
            temp.addClass('required-s');
            setTimeout(function () {
                temp.removeClass('required-s');
            }, 2000);
        });
    }*/
    $(this).removeClass('loading');
});

// Universal-Loader

function loader_start(element, with_parent = true) {

    let self = $(element);
    if (with_parent) {
        self = $(element).parent();
        self.append($('#fountainG').clone().attr('class', 'loader_ajax').attr('id', ''));
        if (self.width() > self.height()) {
            self.find('.loader').width(self.height() - self.height() * 0.10)
            self.find('.loader').height(self.height() - self.height() * 0.10)
        } else {
            self.find('.loader').height(self.width() - self.width() * 0.10)
            self.find('.loader').width(self.width() - self.width() * 0.10)
        }
    } else {
        self.append($('#fountainG').clone().attr('class', 'loader_ajax').attr('id', ''));
        if (self.parent().width() > self.parent().height()) {
            self.find('.loader').width(self.height() - self.height() * 0.10)
            self.find('.loader').height(self.height() - self.height() * 0.10)
        } else {
            self.find('.loader').height(self.width() - self.width() * 0.10)
            self.find('.loader').width(self.width() - self.width() * 0.10)
        }
    }

}

function loader_end() {
    $(".loader_ajax").each((key, value) => {
        console.log(value)
        $(value).remove()
    });
}

// End-Loader

function refresh_total_qty(val = 0) {
    $('#js_cart_items_count').html(val)
}

function refresh_total_price(val = 0) {
    $('.cart_total_price').html(val);
}

async function add_to_cart(content, no_modal = false, redirect = null) {
    return $.ajax({
        type: "POST",
        url: CONFIG_DATA.URLS.add_to_cart,
        data: content,
        success: (data) => {
            if (data.success) {
                M.toast({'html': 'Додано в корзину'});
                $('#cart_toggle .cart_items').html(data.render_html['dropdown']);
                refresh_total_qty(data.cart_items_count);
                console.log('-00000000000000')
                console.log(data.cart_total_price)
                refresh_total_price(data.cart_total_price)
                if (redirect != null) {
                    window.location.href = redirect;
                }
                return true;
            } else {
                if (data.required) {
                    return {'required': data.required}
                }
                if (data.message) {
                    M.toast({'html': data.message});
                }
            }
        }
    })
}

function get_selected_options(product_id, type) {
    let selected_options = [];
    if (type === 'badges') {
        let all_selected_badges = $(`.value.active[data-product-id=${product_id}]`);
        console.log(all_selected_badges)
        $.each(all_selected_badges, function (key, value) {
            selected_options.push({
                'option_pk': $(value).attr('data-option-id'),
                'option_val': $(value).attr('data-value-id'),
            });
        });
    } else {
        let all_options = $('.option-values[data-product-id="' + product_id + '"]');
        $.each(all_options, function (key, value) {
            let option = $(value).find(' option:selected');
            if ($(option).attr('value') !== "-1") {
                selected_options.push({
                    'option_pk': $(value).find(' option:selected').attr('data-option-id'),
                    'option_val': $(value).find(' option:selected').attr('data-value-id'),
                });
            }
        });
    }
    return selected_options;
}

//#endregion CHECKOUT

//#region CALL AFTER LOAD PAGE

//update_attributes(true);

build_price_track();
setTimeout(function () {
    $('body .i4ewOd-pzNkMb-haAclf').remove();
}, 3000);
$(function () {

    function trackScroll() {
        var scrolled = window.pageYOffset;
        var coords = document.documentElement.clientHeight;

        if (scrolled > coords) {
            goTopBtn.classList.remove('scale-out');
        }
        if (scrolled < coords) {
            goTopBtn.classList.add('scale-out');
        }
    }

    function backToTop() {
        if (window.pageYOffset > 0) {
            window.scrollBy(0, -80);
            setTimeout(backToTop, 0);
        }
    }

    var goTopBtn = document.querySelector('#up');

    window.addEventListener('scroll', trackScroll);
    goTopBtn.addEventListener('click', backToTop);
    if ($('#js_category_badges > *').length > 0) {
        $('#js_active_filters_heading').show();
    } else {
        $('#js_active_filters_heading').hide();
    }
    $('[data-fancybox="gallery"]').fancybox({
        padding: 0,
    });
    $("#birthdate").datepicker({
        changeYear: true,
        yearRange: '1910:2010',
        dateFormat: "yy-mm-dd"


    });
    // $(".preloader").hide('fade-out');
    $(".preloader").animate({
            opacity: 0 // прозрачность к нулю к нулю
        }, 400, () => {
            $(".preloader").hide();
        }
    );
    $('.phone_input').each(function () {
        //$(this).mask("+380 (99) 999-99-99");
    });
});
//Скрипт для компютернопго меню
(function ($) {
    $.fn.liMenuHor = function (params) {
        return this.each(function () {
            var
                menuWrap = $(this),
                menuWrapWidth = menuWrap.outerWidth(),
                menuWrapLeft = menuWrap.offset().left,
                menuSub = menuWrap.children('li').children('ul'),
                menuSubSub = $('ul', menuSub);

            menuSub.each(function () {

                var
                    mArrowDown = $('<div>').addClass('arrow-down'),
                    mSub = $(this),
                    mList = $(this).closest('li'),
                    mLink = mList.children('a').append(mArrowDown),
                    mArrow = $('<div>').addClass('arrow-up').prependTo(mSub),
                    mArrow2 = $('<div>').addClass('arrow-up2').prependTo(mSub);

                mLink.on('mouseenter', function () {

                    var
                        mArrowLeft = mLink.outerWidth() / 2 - 5,
                        mSubLeft = mLink.position().left;

                    mSub.css({top: mLink.outerHeight() + mLink.position().top});
                    sum1 = mSubLeft + mSub.outerWidth();
                    if (sum1 > menuWrapWidth) {
                        mSubLeft = mSubLeft - (sum1 - menuWrapWidth);
                        mArrowLeft = mArrowLeft + sum1 - menuWrapWidth;
                        mSub.addClass('toLeft');
                    }
                    mArrow.css({left: mArrowLeft});
                    mArrow2.css({left: mArrowLeft})
                    mSub.css({left: mSubLeft});
                    mSub.show();
                    mLink.addClass('active')
                })
                mList.on('mouseleave', function () {
                    mSub.hide();
                    mLink.removeClass('active');
                })
            })
            menuSubSub.each(function () {

                var
                    mArrowRight = $('<div>').addClass('arrow-right'),
                    mSubSub = $(this),
                    mSubList = mSubSub.closest('li'),
                    mSubLink = mSubList.children('a').append(mArrowRight),
                    mSubArrow = $('<div>').addClass('arrow-left').prependTo(mSubSub),
                    mSubArrow2 = $('<div>').addClass('arrow-left2').prependTo(mSubSub);

                mSubLink.on('mouseenter', function () {
                    mSubArrow.css({top: mSubLink.outerHeight() / 2 - 5});
                    mSubArrow2.css({top: mSubLink.outerHeight() / 2 - 5});
                    var mSubSubLeft = mSubLink.position().left + mSubLink.outerWidth()
                    mSubSub.css({top: (mSubLink.position().top - (mSubLink.closest('ul').outerWidth() - mSubLink.closest('ul').width()) / 2)});
                    mSubSub.css({left: mSubSubLeft});
                    mSubSub.show();

                    var
                        w3 = (menuWrapLeft + menuWrapWidth),
                        w6 = (mSubSub.offset().left + mSubSub.outerWidth());

                    if (w6 >= w3) {
                        mSubSub.closest('ul').addClass('toLeft')
                        mSubSubLeft = -mSubSub.outerWidth()
                    }
                    if (mSubSub.parents('ul').hasClass('toLeft')) {
                        mSubSubLeft = -mSubSub.outerWidth()
                    }
                    mSubSub.css({left: mSubSubLeft});
                    mSubLink.addClass('active')
                })
                mSubList.on('mouseleave', function () {
                    mSubSub.hide();
                    mSubLink.removeClass('active')
                })
            })
            menuWrapWidth = menuWrap.outerWidth();
            menuWrapLeft = menuWrap.offset().left;

            $(window).resize(function () {
                menuWrapWidth = menuWrap.outerWidth();
                menuWrapLeft = menuWrap.offset().left;
            })

        });
    };
})(jQuery);
$('.menu_hor').liMenuHor();
//#endregion CALL AFTER LOAD PAGE

$(document).ready(function () {
    M.AutoInit();
    M.updateTextFields();
    $('.phone_input, .js-phone-input').mask('099 99 99 999');
    $('#quick_order_modal').modal();
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems);

    // let r = $('input#delivery_settlement').autocomplete({
    //     data: {
    //         "Apple": null,
    //         "Microsoft": null,
    //         "Google": 'https://placehold.it/250x250'
    //     },
    // });
});

$(document).ready(function () {
    $('.review_text').each((key, el) => {
        if ($(el).children().height() > 100) {
            $(el).addClass('read-more');
            $(el).removeClass('review_text');
        };
    });
});
