(function ($) {
  $(function () {
    $("#is-multiline-po").on("click", function () {
      var isChecked = $.prop($(this)[0], "checked");
      if (isChecked) {
        $("#singleline").addClass("hidden");
        $("#multiline").removeClass("hidden");
      }
      else {
        $("#multiline").addClass("hidden");
        $("#singleline").removeClass("hidden");
      }
    });

    $("#get-ppoid-early").on("click", function () {
      var isChecked = $.prop($(this)[0], "checked");
      if (isChecked === true && confirm("Are you sure? This will 'reserve' a poid, this cannot be undone")) {
        $.ajax({
          type: "POST",
          url: "/api/v1/purchase/create/interim/"
        }).done(function (data) {
          var pretty_po_id = data.data.pretty_po_id;
          var po_id = data.data.po_id;
          $("#ppoid").html("- PO #" + pad(pretty_po_id, 4));
          $("#_poid").val(po_id);
          $("#get-ppoid-early").attr("disabled", true);
        }).fail(function () {
          alert("We weren't able to retrieve a new PO#, try again later");
        });
      } else {
        $.prop($(this)[0], "checked", false);
      }
    });

    var submitBtn = document.querySelector('#create-form-submit');
    if (submitBtn) {
      submitBtn.addEventListener('click', function (e) {
          e.target.form.submit();
          e.target.disabled = true;
          setTimeout(function () {
            e.target.disabled = false;
          }, 10000);
        }
      );
    }
  }) // End of $(function () {
})(window.jQuery);
