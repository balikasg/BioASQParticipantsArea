$(function() {
  $('#id_test').chainedSelect({
    parent: '#id_task',
    url: 'http://bioasq.lip6.fr/oracle/jsonGen/',
  });
});
