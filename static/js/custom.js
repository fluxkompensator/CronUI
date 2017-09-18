$(document).ready(function(){
    // add new Entries via button
    $( ".add-entry-btn" ).click(function() {
	$( '<a href="#" class="list-group-item list-group-item-danger cron-entry">#* * * * * root ... Empty line</a>' ).insertBefore( this );
	$( '<input type="text" class="cron-edit" style="display:none"/>' ).insertBefore( this );
	$( '<button class="cron-edit cron-delete btn btn-sm btn-warning" style="display:none">Delete entry</button>' ).insertBefore( this );
    });

    // show options/actions for clicked entry
    $(document).on( "click", '.cron-entry', function(){
        $(this).hide().next(".cron-edit").show().val($.trim($(this).text())).focus();
	$(this).next().next(".cron-edit").show();
    });

    // "mousedown" is much better than "onclick/click" it does not interfere with "focusout"
    $(document).on( "mousedown", ".cron-delete", function(){
	$(this).prev().prev(".cron-entry").remove();
	$(this).prev().remove();
	$(this).remove();
    });

    // uncoollapse current item on focusout
    $(".list-group").on('focusout', '.cron-edit', function(){
        $(this).hide().prev(".cron-entry").show().text($(this).val());
	$(this).next('.cron-delete').hide();
	$(this).next('.cron-edit').hide();
    });

    // terminate the edit field by pressing enter
    $(document).on('keypress', '.cron-edit', function( event ){
	if(event.which == 13) {
            $(this).hide().prev(".cron-entry").show().text($(this).val());
    	    $(this).next('.cron-delete').hide();
    	    $(this).next('.cron-edit').hide();
	}
    });

    // save cron entry POST request via AJAX  
    $(function() {
        $('.save-entry-btn').click(function() {
	    var cronEntries = [];
	    $( this ).prevAll(".cron-entry").each( function( index, element ) {
		cronEntries.push($.trim($(this).text()))
	    });
	    var cronTitle = $( this ).closest(".list-group").find("h3").text();
	    cronEntries.push(cronTitle);
            $.ajax({
                url: Flask.url_for('crontabsave'),
		data: JSON.stringify(cronEntries),
                contentType: 'application/json;charset=UTF-8',
                type: 'POST',
                success: function(response) {
		    alert("Crontab "+cronTitle+" saved.");
                },
                error: function(error) {
		    alert("Crontab "+cronTitle+" save failed!");
                }
            });
        });
    });

    // sets active class in navigation item
    $(function() {
        $('nav a[href^="' + location.pathname.split("/")[1] + '"]').addClass('active');
    });
    

});
