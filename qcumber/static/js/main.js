/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$('html').removeClass('no-js').addClass('js');
 
// Enable Dropdown boxes
$('.dropdown-header').click(function () {
    $(this).parent().next().slideToggle('medium');
    return false;
});


// Seasonal Course Filters

$('.season-filter').click(function() {
    var season = $(this).attr('name');
    if ($(this).is(':checked')) {
        $('.course_list .season-' + season).parents('tr').show();
    } else {
        $('.course_list .course').hide();
        $('.season-filter').filter(function() {
            return $(this).is(':checked');
        }).map(function() {
            var season = $(this).attr('name');
            $('.course_list .season-' + season).parents('tr').show();
        });
    }
});


// Enrollment checking button
var subj_abbr = $('.subject-data').data('abbr');
var course_number = $('.course-data').data('number');

$('.check-enrollment').on('click', function (e) {
    //Get data
    var solus_id = $(this).parents('.section-data').data('solus-id');

    var url = "/enrollment/" + subj_abbr + "/" +  course_number + "/" + solus_id +"/";
    var container = $(this).parent();

    //Add a spinner
    $(this).remove();
    container.append('<img src="/static/img/ajax-loader.gif" alt="Loading" height="17" width="17">Gathering enrollment from SOLUS... (May take up to 15s)');

    //Fetch the enrollment data
    container.load(url);

    var label = subj_abbr + " " +  course_number + " (" + solus_id +")";
    _gaq.push(['_trackEvent', "enrollment", "request", label]);
});


// --------------- Google Analytics ---------------

// Track searches
$('.search-form').on('submit', function(e) {
    var form = $(this).parents().hasClass('hero-unit') ? 'index' :
        $(this).parents().hasClass('nav') ? 'search bar' : '???';
    var search_query = $(this).children('[type=search]').val();
    
    _gaq.push(['_trackEvent', 'search', form, search_query]);
    //return false; // for debugging, stops form from submitting.
});

// Outbound Link Tracking
var link_track_event = function(event_name) {
    return function(e){
        var url = $(this).attr("href");
        if (e.currentTarget.host != window.location.host) {

            try { 
                _gaq.push(['_trackEvent', "outbound link", event_name, url]);
            } catch(err){}

            // Checks for control, command, or middle click
            if (e.metaKey || e.ctrlKey || e.which == 2) {
                var newtab = true;
            }
            
            if (!newtab ) {
                e.preventDefault();
                setTimeout('document.location = "' + url + '"', 100);
            }
        }
    }
};

$(function() {
    $(".exams a").on('click', link_track_event("exambank link"));
});
$(function() {
    $(".textbooks a").on('click', link_track_event("textbook link"));
