$( document ).ready(function() {
    function formatState(state) {
        if (!state.id) {
            return state.text;
        }
        var baseUrl = "/static/assets";
        var $state = $(
            '<span><img src="' + baseUrl + '/' + state.element.value.toLowerCase() + '.png" class="img-flag" /> ' + state.text + '</span>'
        );
        return $state;
    };
    // $('.languages').select2({
    //     minimumResultsForSearch: -1,
    //     templateResult: formatState,
    //     templateSelection: formatState,
    // }).on("change", function (e) { 
    //     $.ajax({
    //         type: 'post',
    //         url: '/change_languages/',
    //         data : {
    //             languages : this.value,
    //             csrfmiddlewaretoken: '{{ csrf_token }}',
    //         }
    //     }).then(function (data) {
    //         // create the option and append to Select2
    //         var option = new Option(data.full_name, data.id, true, true);
    //         studentSelect.append(option).trigger('change');
        
    //         // manually trigger the `select2:select` event
    //         studentSelect.trigger({
    //             type: 'select2:select',
    //             params: {
    //                 data: data
    //             }
    //         });
    //     });
    
    // })

  
});