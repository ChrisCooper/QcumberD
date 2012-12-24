/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

 
//Enable Dropdown boxes
$('.dropdown-header').click(function () {
    $(this).parent().next().slideToggle('medium');
    return false;
});





//Enrollment checking button
var subj_abbr = $('.subject-data').data('abbr');
var course_number = $('.course-data').data('number');

$('.check-enrollment').on('click', function (e) {
    var solus_id = $(this).parents('.section-data').data('solus-id');

    var url = "/enrollment/" + subj_abbr + "/" +  course_number + "/" + solus_id +"/";
     $(this).parent().load(url);
})