app.controller('main', function($scope) {

  $scope.callbacks = {
    "next_album" : function(data) {
      data = JSON.parse( data );
      if( data && data["output"] ) {
        $scope.current = data["output"];
      }
    },
    
    "prev_album" : function(data) {
      data = JSON.parse( data );
      if( data && data["output"] ) {
        $scope.current = data["output"];
      }
    },    
  }
  
  $scope.playLists = [];
  $scope.current = "";
  $scope.requests = [];
  $scope.isShuffled = false;
  $scope.isPlaying = false;
   
  // Perform a network action with the server
  $scope.playerAction = function( action, callback) {
    if( typeof callback === "undefined" ) {
      callback = function(d){ console.log(d); };
    }
    
    var request = $.ajax({
      type: "POST",
      url: "index.html",
      data: { action: action }
    })
    .done(callback)
    .always(function(data){
      // Provide a action callback if it is defined
      if( typeof $scope.callbacks[action] === "function" ) {
        $scope.callbacks[action]( data );
      }
      $scope.requests.pop();
      $scope.$apply();
    });
    
    $scope.requests.push( request );
  };
  
  $scope.syncPlayer = function(){
    $scope.playerAction( "info", function(data){
      data = JSON.parse( data );
      if( data && data["output"] ) {
        console.log( data );
      }
    });
  };
  
  $scope.updatePlaylist = function(){
    $scope.playerAction( "info_playlists", function(data){
      data = JSON.parse( data );
      if( data && data["output"] ) {
        $scope.playLists = data["output"]["lists"];
        $scope.current = data["output"]["current"];
        $scope.$apply();
      }
    });
  };
  
  $scope.updatePlaylist();
  $scope.syncPlayer();
});
