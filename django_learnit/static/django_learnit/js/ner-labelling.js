$(document).ready(function () {

  var tokens = $('.token');
  var labels = $('input[name$="-label"]');

  var startIndex = null,
      endIndex = null;

  /**
   * Updates tokens `data-label` using form data
   */
  function updateTokens () {
    $('.token').each(function (index) {
      var label = $('input[name$="' + index + '-label"]').val();
      $(this).attr('data-label', label);
    });

    // Focus submit to allow quick form submit with Enter
    $('input[type="submit"]').focus();
  }

  /**
   * Sets labels for a selection range
   */
  function setLabels(start, end, label) {
    for (var i = start; i <= end; i++) {
      $(labels[i]).val(label);
    }
    updateTokens();
  }

  /**
   * Adds selected feedback class on tokens
   */
  function updateSelectionFeedback () {
    tokens.removeClass('selected');

    var start = Math.min(startIndex, endIndex);
    var end = Math.max(startIndex, endIndex);

    for (var i = start; i <= end; i++) {
      $(tokens[i]).addClass('selected');
    }
  }

  // Update tokens on labels change
  labels.change(function () {
    updateTokens();
  });

  // Start selection
  tokens.mousedown(function () {
    var index = $(this).data('index');

    startIndex = parseInt(index);
    endIndex = parseInt(index);

    updateSelectionFeedback();
  });

  // Update selection
  tokens.mouseenter(function () {
    if (startIndex !== null) {
      endIndex = parseInt($(this).data('index'));
      updateSelectionFeedback();
    }
  });

  tokens.mouseleave(function () {

  })

  // End selection
  $(document).mouseup(function () {
    if (startIndex !== null && endIndex !== null) {
      var start = Math.min(startIndex, endIndex);
      var end = Math.max(startIndex, endIndex);

      // Get end element position
      var el = $(tokens[endIndex]);

      $('ul.classes')
        .attr({
          'data-start': start,
          'data-end': end
        })
        .css({
          'top': (el.outerHeight() + el.offset()['top'] + 2) + 'px',
          'left': el.offset()['left'] + 'px'
        })
        .show();

      startIndex = null;
      endIndex = null;
    } else {
      // Reset
      $('ul.classes').hide();
      tokens.removeClass('selected');
      $('input[type="submit"]').focus();
    }
  });

  // Set selection
  $('.classes > li').click(function () {
    var start = parseInt($(this).parent().attr('data-start'));
    var end = parseInt($(this).parent().attr('data-end'));
    setLabels(start, end, $(this).data('label'));
  });

  // Setup
  updateTokens();

});
