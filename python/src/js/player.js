(function(){

  var processTime = function(t) {
      var result = null;

      if( t && typeof t === "string" ) {
        var comps = t.split(":");
        if( comps.length == 2 ) {
          result = parseInt(comps[0])*60 + parseInt(comps[1]);
        }
      }

      return result;
  }

  app.controller('main', function($scope) {

    $scope.currentState = {};
    $scope.requests = [];
    $scope.syncHandle = null;
    $scope.requestUrl = "/";

    // Get the saved requestUrl from localstorage if it exists
    if( localStorage ) {
      var item;
      if( item = localStorage.getItem("MP3-OVERRIDE-URL")) {
        $scope.requestUrl = item;
      }
    }

    $scope.computeDuration = function() {
      var currentTime = processTime( $scope.currentState.currenttime ),
          totalTime = processTime( $scope.currentState.totaltime ),
          result = 0;

      if( currentTime !== null && totalTime !== null ) {
        result = currentTime / totalTime * 100;
      }

      return result + "%";
    }

    $scope.getProgressText = function() {
      var result = "- No Title -";

      if( $scope.currentState["title"] ) {
        result = $scope.currentState["title"];
      }

      return result;
    }

    // Wrapper for button clicks to disable actions
    // until all of the requests are resolved
    $scope.buttonPlayerAction = function( action, callback ) {
      if( !$scope.requests.length ) {
        $scope.playerAction( action, callback )
      }
    }

    // Perform a network action with the server
    $scope.playerAction = function( action, callback) {
      if( typeof callback === "undefined" ) {
        callback = function(d){ console.log(d); };
      }

      var request = $.ajax({
        type: "POST",
        url: $scope.requestUrl,
        data: { action: action },
        timeout: 5000
      })
      .done(callback)
      .always(function(data){
        // Sync the player if this was not a info action
        if( action !== "info" ) {
          setTimeout( function() {
            $scope.syncPlayer();
          }, 250 );
        }
        $scope.requests.pop();
        $scope.$apply();
      });

      $scope.requests.push( request );
    };

    $scope.syncPlayer = function(){
      $scope.playerAction( "info", function(data){
        if( data && data["output"] ) {
          clearTimeout( $scope.syncHandle );
          $scope.syncHandle = setTimeout( $scope.syncPlayer, 8000 );
          $scope.currentState = data["output"];
          $scope.$apply();
        }
      });
    };

    $scope.syncPlayer()
  });
})()
