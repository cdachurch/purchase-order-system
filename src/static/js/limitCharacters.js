(function ($) {
  'use strict';

  $('#multiline-product').on('keydown blur', function (e) {
    var $textArea = $(e.currentTarget);
    var $warningDiv = $('#text-too-long');
    var $createFormSubmitBtn = $('#create-form-submit');

    if ($textArea.val().length >= 500) {
      $('#characters').html($textArea.val().length);
      $warningDiv.removeClass('hidden');
      $createFormSubmitBtn.prop('disabled', true);
    } else {
      if (!$warningDiv.hasClass('hidden')) {
        $warningDiv.addClass('hidden');
      }
      $createFormSubmitBtn.prop('disabled', false);
    }
  });
} (window.jQuery));
