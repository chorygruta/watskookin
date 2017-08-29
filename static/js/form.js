$(document).ready(function() {

	$('form').on('submit', function(event) {

		$.ajax({
			data : {
				ingredient : $('#ingredientInput').val()
        alert($('#ingredientInput').val());
			},
      type : 'POST',
			url : '/process'
		})
		.done(function(data) {

			alert('works');

		});

		event.preventDefault();

	});

});
