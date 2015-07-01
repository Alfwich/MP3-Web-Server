app.controller('main', function($scope) {

  $scope.playLists = [];
  $scope.currentPlaylist = "";
  $scope.currentSongName = "";
  $scope.requests = [];
  $scope.isShuffled = false;
  $scope.isPlaying = false;

  $scope.callbacks = {
    "next_album" : function(data) {
      data = JSON.parse( data );
      if( data && data["output"] ) {
        $scope.currentPlaylist = data["output"];
      }
    },
    
    "prev_album" : function(data) {
      data = JSON.parse( data );
      if( data && data["output"] ) {
        $scope.currentPlaylist = data["output"];
      }
    },

    "refresh_data" : function() {
      $scope.updatePlaylist();
    }

  }
   
  // Perform a network action with the server
  $scope.playerAction = function( action, callback) {
    if( typeof callback === "undefined" ) {
      callback = function(d){ console.log(d); };
    }
    
    var request = $.ajax({
      type: "POST",
      url: "index.html",
      data: { action: action },
      timeout: 1500
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
    console.log( "Sync!" );
    $scope.playerAction( "info", function(data){
      data = JSON.parse( data );
      if( data && data["output"] ) {
        $scope.currentSongName = data["output"]["songtitle"];
        $scope.$apply();
      }
    });
  };
  
  $scope.updatePlaylist = function(){
    $scope.playerAction( "info_playlists", function(data){
      data = JSON.parse( data );
      if( data && data["output"] ) {
        $scope.playLists = data["output"]["lists"];
        $scope.currentPlaylist = data["output"]["current"];
        $scope.$apply();
      }
    });
  };
  
  $scope.updatePlaylist();
  $scope.syncPlayer();
  setInterval( $scope.syncPlayer, 2000 );

});
