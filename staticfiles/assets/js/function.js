$(document).ready(function (){

    // Function to get CSRF token from the cookies
    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

    $(".filter-checkbox, #price-filter-btn").on("click", function(){
        console.log("A checkbox has been clicked");

        let filter_object = {}

        let min_price = $("#max_price").attr("min")
        let max_price = $("#max_price").val()

        filter_object.min_price = min_price;
        filter_object.max_price = max_price;

        // Loop through filter checkboxes
        $(".filter-checkbox").each(function(){
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter") // vendor, category

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function(element){
                return element.value;
            });
        });

        console.log("Filter Object is: ", filter_object);

        // AJAX request for filtering products
        $.ajax({
            url: '/filter-products',
            data: filter_object,
            dataType: 'json',
            headers: {
                'X-CSRFToken': getCSRFToken()  // Include CSRF token in the header
            },
            beforeSend: function(){
                console.log("Trying to filter products...");
            },
            success: function(response){
                console.log("Data filtered successfully...");
                $(".totall-product").hide();
                $("#filtered-product").html(response.data);
            },
            error: function(xhr, status, error) {
                console.error("Error occurred: ", status, error);
            }
        });
    });

    // Price range validation
    $("#max_price").on("blur", function(){
        let min_price = $(this).attr("min");
        let max_price = $(this).attr("max");
        let current_price = $(this).val();

        if (current_price < parseInt(min_price) || current_price > parseInt(max_price)){
            min_price = Math.round(min_price * 100) / 100;
            max_price = Math.round(max_price * 100) / 100;

            alert("Price must be between $" + min_price + " and $" + max_price);
            $(this).val(min_price);
            $('#range').val(min_price);
            $(this).focus();
            return false;
        }
    });
});
