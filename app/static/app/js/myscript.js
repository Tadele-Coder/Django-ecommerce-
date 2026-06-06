// PLUS CART
$('.plus-cart').click(function () {

    var id = $(this).attr('pid');
    var quantityElement = $(this).siblings('.quantity');

    $.ajax({
        type: 'GET',
        url: '/pluscart/',
        data: {
            prod_id: id
        },

        success: function (data) {

            quantityElement.text(data.quantity);

            $('#amount').text(data.amount + ' BIRR');
            $('#totalamount').text(data.totalamount + ' BIRR');
        }
    });
});


// MINUS CART
$('.minus-cart').click(function () {

    var id = $(this).attr('pid');
    var quantityElement = $(this).siblings('.quantity');

    $.ajax({
        type: 'GET',
        url: '/minuscart/',
        data: {
            prod_id: id
        },

        success: function (data) {

            if (data.quantity == 0) {
                location.reload();
            } else {
                quantityElement.text(data.quantity);
            }

            $('#amount').text(data.amount + ' BIRR');
            $('#totalamount').text(data.totalamount + ' BIRR');
        }
    });
});


// REMOVE CART
$('.remove-cart').click(function () {

    var id = $(this).attr('pid');
    var element = $(this);

    $.ajax({
        type: 'GET',
        url: '/removecart/',
        data: {
            prod_id: id
        },

        success: function (data) {

           $('#amount').text(data.amount + ' BIRR');
            $('#totalamount').text(data.totalamount + ' BIRR');

            element.closest('.row').remove();

            if (data.amount == 0) {
                location.reload();
            }
        }
    });
});

$(document).on('click', '.plus-wishlist', function(){

    var id = $(this).attr('pid').toString();
    var eml = this;

    $.ajax({
        type: 'GET',
        url: '/pluswishlist',
        data: {
            prod_id: id
        },
        success: function(data){

            $(eml).removeClass('plus-wishlist btn-success');
            $(eml).addClass('minus-wishlist btn-danger');

        }
    });

});


$(document).on('click', '.minus-wishlist', function(){

    var id = $(this).attr('pid').toString();
    var eml = this;

    $.ajax({
        type: 'GET',
        url: '/minuswishlist',
        data: {
            prod_id: id
        },
        success: function(data){

            $(eml).removeClass('minus-wishlist btn-danger');
            $(eml).addClass('plus-wishlist btn-success');

        }
    });

});