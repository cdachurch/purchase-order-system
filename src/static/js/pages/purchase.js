(function ($, templateData) {
  $(function () {
    var $acceptButton = $("#accept-btn");
    var $denyButton = $("#deny-btn");
    var $cancelButton = $("#cancel-btn");

    $acceptButton.click(function () {
      var acceptLink = "/api/v1/purchase/accept/" + templateData.poId + "/";
      addressRequest(acceptLink);
    });
    $denyButton.click(function () {
      var denyLink = "/api/v1/purchase/deny/" + templateData.poId + "/";
      addressRequest(denyLink);
    });
    $cancelButton.click(function () {
      var cancelLink = "/api/v1/purchase/cancel/" + templateData.poId + "/";
      addressRequest(cancelLink);
    });

    var addressRequest = function (link) {
      $.ajax({
        type: "GET",
        url: link
      }).done(function () {
        // alert("The request was affected successfully.");
        location.reload();
      }).fail(function () {
        alert("There was a problem, please contact gholtslander@cdac.ca");
      });
    };

    $("input[type=checkbox]").click(function () {
      var poId = $(this)[0].value;
      $.ajax({
        type: "GET",
        url: "/api/v1/purchase/invoice/" + poId + "/"
      }).done(function () {
        // pass
      }).fail(function () {
        alert("There was a problem, try again in a few minutes");
        $("#invoice-done").prop("checked", false);
      });
    });
  });
})(window.jQuery, window.templateData);
