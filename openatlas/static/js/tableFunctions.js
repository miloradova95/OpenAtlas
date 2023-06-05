async function showTableModal(fieldId, filterIds) {
  $(`#${ fieldId }-modal`).modal('show');

  await loadModalTable(fieldId, filterIds);
}

async function loadModalTable(fieldId, filterIds) {
    if (setTableModalLoading(fieldId)) {
      const tableContent = await getTableContent(fieldId, filterIds);
      fillTable(fieldId, tableContent);
      return tableContent;
    }
    return null;
}

function setTableModalLoading(fieldId) {
  const modalTable = $(`#${fieldId }-modal .modal-body-table`);
  if(modalTable.is(':empty')) {
    modalTable.append(
        '<div class="mx-auto mt-5 mb-5 text-center">' +
        ' <span ' +
        '   class="spinner-border spinner-border-sm" ' +
        '   role="status" ' +
        '   aria-hidden="true"></span>' +
        ' Loading...</div>');
      return true;
  }
  return false;
}

function tableIsEmpty(fieldId) {
  const modalTable = $(`#${fieldId }-modal .modal-body-table`);
  return modalTable.is(':empty');
}

async function getTableContent(id, filterIds) {
  const tableContent = await $.ajax({
    type: 'post',
    url: `/ajax/get_entity_table/${id}`,
    data: {filterIds: JSON.stringify(filterIds)},
  });
  return tableContent;
}

async function refillTable(id, filterIds = []) {
  const tableContent = await getTableContent(id, filterIds);

  fillTable(id, tableContent);
}

function fillTable(id, tableContent) {
  const table = clearTable(id);
  table.append($(`${tableContent}`));
  return table;
}

function clearTable(fieldId) {
  const table = $(`#${fieldId}-modal .modal-body-table`);
  table.empty();
  return table;
}

async function setupTable(fieldId, filterIds) {
    if(!tableIsEmpty(fieldId)) {
      return;
    }

    loadModalTable(fieldId, filterIds);
}


function selectFromTable(element, table, id,label= undefined) {
  $("#" + table).attr('value', id);
  $("#" + table + "-button").val(label || element?.innerText );
  $("#" + table + "-button").focus(); /* to refresh/fill button and remove validation errors */
  $("#" + table + "-clear-field").show();
  $('#' + table + '-modal').modal('hide');
}

function deselectFromTable(tableName, nodeId) {
  $(`#${tableName}_table`)?.find(`#${nodeId}[type="checkbox"]`)?.prop( "checked", false )
  selectFromTableMulti(tableName)
}

function selectFromTableMulti(name) {
  let checkedNames = [];
  let ids = [];
  $('#' + name + '_table').DataTable().rows().nodes().to$().find('input[type="checkbox"]').each(
    function () {
      if ($(this).is(':checked')) {
        checkedNames.push({name:$(this).val(),id:$(this).attr('id')});
        ids.push($(this).attr('id'));
      }
    });
  $('#' + name + '-selection')
      .html(checkedNames.map(x => closableBadge(x.name,`deselectFromTable('${name}',${x.id})`)));
  $('#' + name).val(ids.length > 0 ? '[' + ids + ']' : '').trigger('change');
}
