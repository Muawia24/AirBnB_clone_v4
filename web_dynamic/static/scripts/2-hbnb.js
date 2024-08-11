$('document').ready(function () {
  $('input[type="checkbox"]').click(function () {
    const amenityId = [];
    const amenityName = [];

    $('input[type="checkbox"]:checked').each(function () {
      amenitId.push($(this).attr('data-id'));
      amenityName.push($(this).attr(data - name));
    });
    if (amenityName.length === 0) {
      $('.amenities h4').html('&nbsp;');
    } else {
      $('.amenities h4').text(amenityName.join(', '));
    }
    console.log(amenityId);
  });
});

$.ajax({
  url: 'http://0.0.0.0:5001/api/v1/status/',
  type: 'GET',
  dataType: 'json',
  success: function (json) {
    $('div#api_status').addClass('available');
  },
  error: function (xhr, status) {
    		console.log('error ' + status);
  }
});
