
$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();
    $('#readMore').hide();
    $('#more-section').hide();

    // Upload Preview
    function readURL(input){
    if (input.files && input.files[0]) {
        var reader=new FileReader();

        reader.onload=function (e) {
            $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
            $('#imagePreview').hide();
            $('#imagePreview').fadeIn(650);
        }

        reader.readAsDataURL(input.files[0]);
    }
}


// to structure the disease details taken from json
function structureData(obj){
    for(const key in obj){
        const value = key.slice(2)
        $('#detail').append('<h5><strong>'+value+'</strong></h5>')
        if(typeof obj[key] === 'object' && !Array.isArray(obj[key])){
            for(const key1 in obj[key]){
                $("#detail").append('<strong>'+key1+' : </strong> '+obj[key][key1]+'</br>')
            }
        }else if(typeof obj[key] === 'string'){
            $("#detail").append(obj[key]+'</br>')
        }else if(typeof obj[key] === 'object'){
            for(const str in obj[key]){
                $("#detail").append('<li>'+obj[key][str]+'</li>')
            }
        }
        $("#detail").append('</br>')
    }
}

    $("#imageUpload").change(function () {
            $('.drop-area').hide();
            $('.msg').hide();
            $('.image-section').show();
            $('#btn-predict').show();
            $('#result').text('');
            $('#result').hide();
            $('#readMore').hide();
            $('#more-section').hide();
            readURL(this);
        });

    // Predict
    $('#btn-predict').click(function () {
            var form_data=new FormData($('#upload-file')[0]);

            // Show loading animation
            $(this).hide();
            $('.loader').show();

            // Make prediction by calling api /predict
            $.ajax({

                type: 'POST',
                url: '/predict',
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
                async: true,
                success: function (data) {
                    // Get and display the result
                    $('.loader').hide();
                    $('#result').fadeIn(600);
                    $('#result').text(' Result:  ' + data[0]);
                    $('#dname').text(data[2])
                    $('#detail').text()
                    structureData(data[1])
                    $('#readMore').show();
                    $('#more-section').show();
                    console.log('Success!');
                }

                ,
            });
    });

    $('#readMore').click(()=>{
        $('#more-section').toggleClass('d-none')
        let txt = $('#readMore').text();
        if(txt == 'Read More'){
            $('#readMore').text('Hide');
        }else{
            $('#readMore').text('Read More');
        }
    })

});



