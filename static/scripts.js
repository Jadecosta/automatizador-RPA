// operacionalização

// Função para popular os tipos de operacionalização baseados no módulo selecionado
function populateOperationTypes() {
    let moduleSelect = document.getElementById('module');
    let operationTypeSelect = document.getElementById('operation-type');
    operationTypeSelect.innerHTML = ''; // Limpa as opções atuais

    if (moduleSelect.value === 'pessoas') {
        let options = ['Ingresso', 'Promoção' ,'Lotação', /*'Inclusão Perfil', 'Alterar Dados',*/ 'Desligamento'];
        options.forEach(option => {
            let opt = document.createElement('option');
            opt.text = option;
        
            // Normalização completa do value
            opt.value = option
                .toLowerCase()
                .normalize("NFD")                // Separa os acentos
                .replace(/[\u0300-\u036f]/g, '') // Remove acentos
                .replace(/[^a-z0-9\s]/g, '')     // Remove caracteres especiais
                .trim()
                .replace(/\s+/g, '_');           // Substitui espaços por underline
        
            operationTypeSelect.add(opt);
        });
    } /*else if (moduleSelect.value === 'seguranca') {
        let options = ['Excluir Permissões'];
        options.forEach(option => {
            let opt = document.createElement('option');
            opt.text = option;
            opt.value = option.toLowerCase().replace(/\s+/g, '_');
            operationTypeSelect.add(opt);
        });
    }*/ else if (moduleSelect.value === 'folha') {
        let options = ['Incluir Servidor', 'Importar Ger. Ev. Cal.'];
        options.forEach(option => {
            let opt = document.createElement('option');
            opt.text = option;
        
            // Normalização completa do value
            opt.value = option
                .toLowerCase()
                .normalize("NFD")                // Separa os acentos
                .replace(/[\u0300-\u036f]/g, '') // Remove acentos
                .replace(/[^a-z0-9\s]/g, '')     // Remove caracteres especiais
                .trim()
                .replace(/\s+/g, '_');           // Substitui espaços por underline
        
            operationTypeSelect.add(opt);
        });
    } else if (moduleSelect.value === 'funprev') {
        let options = ['Ingresso Pecunia', 'Aposentadoria'];
        options.forEach(option => {
            let opt = document.createElement('option');
            opt.text = option;
        
            // Normalização completa do value
            opt.value = option
                .toLowerCase()
                .normalize("NFD")                // Separa os acentos
                .replace(/[\u0300-\u036f]/g, '') // Remove acentos
                .replace(/[^a-z0-9\s]/g, '')     // Remove caracteres especiais
                .trim()
                .replace(/\s+/g, '_');           // Substitui espaços por underline
        
            operationTypeSelect.add(opt);
        });
    } /*else if (moduleSelect.value === 'tabelas_basicas') {
        let options = ['Organograma'];
        options.forEach(option => {
            let opt = document.createElement('option');
            opt.text = option;
            opt.value = option.toLowerCase().replace(/\s+/g, '_');
            operationTypeSelect.add(opt);
        });
    }*/ 
}

// mapa de endpoint
const endpointsMap = {
    'pessoas_ingresso': '/scripts/script_ingresso.py',
    'pessoas_promocao': '/scripts/script_promocao.py',
    'pessoas_lotacao': '/scripts/script_lotacao.py',
    'pessoas_inclusao_perfil': '/scripts/script_inclusao_perfil.py',
    'pessoas_alterar_dados': '/scripts/script_dados_regime.py',
    'pessoas_desligamento': '/scripts/script_desligamento.py',
    'tabelas_basicas_organograma': '/scripts/script_organograma.py',
    'folha_importar_ger._ev._cal.': '/scripts/script_ger_ev_cal.py',
    'folha_incluir_servidor': '/scripts/script_incluir_servidor.py',
    'seguranca_excluir_permissoes': '/scripts/script_excluir_permissoes.py',
    'funprev_ingresso_pecunia': '/scripts/script_ingresso_pecunia.py',
    'funprev_aposentadoria': '/scripts/script_aposentadoria.py'
};

async function executeScript() {
    // Obter os valores de usuário, senha e arquivo
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;
    let fileInput = document.getElementById('file-upload');
    let file = fileInput.files[0];
    let module = document.getElementById('module').value;
    let operationType = document.getElementById('operation-type').value;

    // Validação simples
    if (!username || !password || !file || !module || !operationType) {
        alert("Por favor, preencha todos os campos e selecione um arquivo.");
        return;
    }

    // Chamada a um endpoint para executar o script
    let endpoint = '';
    if (module === 'pessoas' && operationType === 'ingresso') {
        endpoint = '/scripts/script_ingresso.py';
    } else if (module === 'pessoas' && operationType === 'promocao') {
        endpoint = '/scripts/script_promocao.py';
    } else if (module === 'pessoas' && operationType === 'lotação') {
        endpoint = '/scripts/script_lotacao.py';
    } else if (module === 'pessoas' && operationType === 'inclusao_perfil') {
        endpoint = '/scripts/script_inclusao_perfil.py';
    } else if (module === 'pessoas' && operationType === 'alterar_dados') {
        endpoint = '/scripts/script_dados_regime.py';
    } else if (module === 'pessoas' && operationType === 'desligamento') {
        endpoint = '/scripts/script_desligamento.py';
    } else if (module === 'tabelas_basicas' && operationType === 'organograma') {
        endpoint = '/scripts/script_organograma.py';
    } else if (module === 'folha' && operationType === 'importar_ger._ev._cal.') {
        endpoint = '/scripts/script_ger_ev_cal.py';
    } else if (module === 'folha' && operationType === 'incluir_servidor') {
        endpoint = '/scripts/script_incluir_servidor.py';
    } else if (module === 'seguranca' && operationType === 'excluir_permissoes') {
        endpoint = '/scripts/script_excluir_permissoes.py';
    } else if (module === 'funprev' && operationType === 'ingresso_pecunia') {
        endpoint = '/scripts/script_ingresso_pecunia.py';
    } else if (module === 'funprev' && operationType === 'aposentadoria') {
        endpoint = '/scripts/script_aposentadoria.py';
    } 

    if (!endpoint) {
        alert("Operação ou módulo inválido.");
        return;
    }

    // Preparar os dados para envio
    let formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    formData.append('file', file);

    try {
        // Chamada ao backend
        let response = await fetch(endpoint, {
            method: 'POST',
            body: formData
        });

        let result = await response.json();

        if (response.ok) {
            alert(result.message || "Script executado com sucesso!");
            console.log("Task ID:", result.task_id);
            localStorage.setItem('currentTaskId', result.task_id);
        
            // Inicia o polling para verificar o progresso
            const intervalId = setInterval(async () => {
                try {
                    let progressResponse = await fetch(`/progress/${taskId}`);
        
                    if (!progressResponse.ok) {
                        throw new Error('Erro ao buscar o progresso.');
                    }
        
                    let progressData = await progressResponse.json();
        
                    let progressBar = document.getElementById('progress-bar');
                    let progressText = document.getElementById('progress-text');
        
                    if (progressBar && progressText) {
                        progressBar.style.transition = "width 1s"; // Transição suave
                        progressBar.value = progressData.progress;
                        progressText.textContent = `${progressData.progress.toFixed(2)}%`;
                    } else {
                        console.warn('Elementos da barra de progresso não encontrados.');
                    }
        
                    if (progressData.progress >= 100) {
                        clearInterval(intervalId);
                        renderPage();
                    }
                } catch (progressError) {
                    console.error('Erro durante o polling de progresso:', progressError);
                    clearInterval(intervalId); // Encerra o polling em caso de erro
                    alert("Erro ao verificar o progresso.");
                }
            }, 5000); // Polling a cada 5 segundos
        
        } else {
            alert("Erro: " + (result.message || "Falha ao executar o script."));
        }
    } catch (error) {
        console.error('Erro na execução:', error);
        alert("Ocorreu um erro na comunicação com o servidor.");
    }
}

async function stopScript() {
    let taskId = localStorage.getItem('currentTaskId'); // Recupera o ID do script atual

    if (!taskId) {
        alert("Nenhum script em execução para interromper.");
        return;
    }

    console.log("Task ID recuperado:", taskId); // Adicionado para depuração

    try {
        let response = await fetch(`/stop_script/${taskId}`, {
            method: 'POST'
        });

        if (response.ok) {
            let result = await response.json();
            console.log(result);
            alert("Script interrompido com sucesso!");
            localStorage.removeItem('currentTaskId');
        } else {
            alert("Erro ao interromper o script.");
        }
    } catch (error) {
        console.error("Erro:", error);
        alert("Erro ao tentar interromper o script.");
    }
}


function updateDownloadLink() {
    var module = document.getElementById("module").value;
    var tipo = document.getElementById("operation-type").value;
    var downloadLink = document.getElementById("downloadLink");

    if (module === "pessoas" && tipo === "ingresso") {
        downloadLink.href = "/download/modelo_ingresso.xlsx";
        downloadLink.style.display = "inline";
    } else if (module === "pessoas" && tipo === "promoção") {
        downloadLink.href = "/download/modelo_promocao.xlsx";
        downloadLink.style.display = "inline";
    } else if (module === "pessoas" && tipo === "lotação") {
        downloadLink.href = "/download/modelo_lotacao.xlsx";
        downloadLink.style.display = "inline";
    } else if (module === "pessoas" && tipo === "inclusão_perfil") {
        downloadLink.href = "/download/modelo_inclusao_perfil.xlsx";
        downloadLink.style.display = "inline";
    } else if (module === "pessoas" && tipo === "alterar_dados") {
        downloadLink.href = "/download/modelo_alterar_dados.xlsx";
        downloadLink.style.display = "inline";
    } else if (module === "pessoas" && tipo === "desligamento") {
        downloadLink.href = "/download/modelo_desligamento.xlsx";
        downloadLink.style.display = "inline";
    } else if (module === "tabelas_basicas" && tipo === "organograma") {
        downloadLink.href = "/download/modelo_organograma.xlsx";
        downloadLink.style.display = "inline";
    } else if (module === "folha" && tipo === "importar_ger._ev._cal.") {
        downloadLink.href = "/download/modelo_ger_ev_cal.xlsx";
        downloadLink.style.display = "inline";
    } else if (module === "folha" && tipo === "incluir_servidor") {
        downloadLink.href = "/download/modelo_incluir_servidor.xlsx";
        downloadLink.style.display = "inline";
    } else if (module === "seguranca" && tipo === "permissões_individuais") {
        downloadLink.href = "/download/modelo_permissoes_individuais.xlsx";
        downloadLink.style.display = "inline";
    } else if (module === "seguranca" && tipo === "excluir_permissões") {
        downloadLink.href = "/download/modelo_excluir_permissoes.xlsx";
        downloadLink.style.display = "inline";
    } else if (module === "funprev" && tipo === "ingresso_pecunia") {
        downloadLink.href = "/download/modelo_ingresso_pecunia.xlsx";
        downloadLink.style.display = "inline";
    } else if (module === "funprev" && tipo === "aposentadoria") {  
        downloadLink.href = "/download/modelo_aposentadoria.xlsx";
        downloadLink.style.display = "inline";
    } else {
        downloadLink.style.display = "none";
    }
}

/////////////////////////////////////////////////////
/////////////////// HISTÓRICO///////////////////////
////////////////////////////////////////////////////

document.addEventListener("DOMContentLoaded", function() {
    fetchHistoryData();
});

// Variáveis de paginação
let currentPage = 1;
const itemsPerPage = 20;
let historyData = [];

async function fetchHistoryData() {
    try {
        let response = await fetch('/historico/data');
        if (response.ok) {
            historyData = await response.json();
            console.log("Dados carregados:", historyData); // Verificar se os dados chegaram corretamente

            if (historyData.length > 0) {
                updatePagination();
                populateHistoryTable();
            } else {
                console.warn("Nenhum dado encontrado!");
                document.getElementById('history-table').getElementsByTagName('tbody')[0].innerHTML = '<tr><td colspan="5">Nenhum dado encontrado</td></tr>';
            }
        } else {
            console.error('Erro ao buscar dados do histórico.');
        }
    } catch (error) {
        console.error('Erro:', error);
    }
}

function paginateHistory() {
    let tbody = document.getElementById('history-table').getElementsByTagName('tbody')[0];
    tbody.innerHTML = ''; // Limpa a tabela antes de preencher novamente

    let start = (currentPage - 1) * itemsPerPage;
    let end = start + itemsPerPage;
    let paginatedData = historyData.slice(start, end);

    paginatedData.forEach(item => {
        addToHistory(item.username, item.operation_type, item.date_time, item.file_name, item.log_file_name);
    });
}

function renderPagination() {
    let totalPages = Math.ceil(historyData.length / itemsPerPage);
    let paginationDiv = document.getElementById("pagination-controls");
    paginationDiv.innerHTML = '';

    let prevButton = document.createElement("button");
    prevButton.textContent = "Anterior";
    prevButton.disabled = currentPage === 1;
    prevButton.onclick = function() {
        if (currentPage > 1) {
            currentPage--;
            paginateHistory();
            renderPagination();
        }
    };
    paginationDiv.appendChild(prevButton);

    for (let i = 1; i <= totalPages; i++) {
        let pageButton = document.createElement("button");
        pageButton.textContent = i;
        pageButton.classList.add("page-btn");
        if (i === currentPage) {
            pageButton.classList.add("active");
        }
        pageButton.onclick = function() {
            currentPage = i;
            paginateHistory();
            renderPagination();
        };
        paginationDiv.appendChild(pageButton);
    }

    let nextButton = document.createElement("button");
    nextButton.textContent = "Próximo";
    nextButton.disabled = currentPage === totalPages;
    nextButton.onclick = function() {
        if (currentPage < totalPages) {
            currentPage++;
            paginateHistory();
            renderPagination();
        }
    };
    paginationDiv.appendChild(nextButton);
}

function populateHistoryTable() {
    let tbody = document.getElementById('history-table').getElementsByTagName('tbody')[0];
    tbody.innerHTML = ''; // Limpa a tabela antes de adicionar novos dados

    // Verifica se há dados disponíveis
    if (historyData.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5">Nenhum dado disponível</td></tr>';
        return;
    }

    // Calcula os índices para exibir os itens da página atual
    let startIndex = (currentPage - 1) * itemsPerPage;
    let endIndex = startIndex + itemsPerPage;
    let paginatedData = historyData.slice(startIndex, endIndex);

    console.log("Exibindo itens:", paginatedData); // Depuração para verificar os dados exibidos

    // Preenche a tabela com os dados da página atual
    paginatedData.forEach(item => {
        addToHistory(item.username, item.operation_type, item.date_time, item.file_name, item.log_file_name);
    });

    // Atualiza os controles de paginação
    updatePagination();
}

function addToHistory(username, operationType, dateTime, fileName, logFileName) {
    let tbody = document.getElementById('history-table').getElementsByTagName('tbody')[0];
    let newRow = tbody.insertRow();

    newRow.insertCell().textContent = username;
    newRow.insertCell().textContent = operationType;
    newRow.insertCell().textContent = dateTime;

    let fileNameCell = newRow.insertCell();
    let downloadFileButton = document.createElement('a');
    downloadFileButton.textContent = 'Download';
    downloadFileButton.href = `/uploads/${fileName}`;
    downloadFileButton.setAttribute('download', '');
    downloadFileButton.classList.add('download-button');
    fileNameCell.appendChild(downloadFileButton);

    let logFileNameCell = newRow.insertCell();
    let downloadLogButton = document.createElement('a');
    downloadLogButton.textContent = 'Download';
    downloadLogButton.href = `/logs/${logFileName}`;
    downloadLogButton.setAttribute('download', '');
    downloadLogButton.classList.add('download-button');
    logFileNameCell.appendChild(downloadLogButton);
}

function updatePagination() {
    let totalPages = Math.ceil(historyData.length / itemsPerPage);
    document.getElementById('page-info').textContent = `Página ${currentPage} de ${totalPages || 1}`;

    document.getElementById('prev-page').disabled = currentPage === 1;
    document.getElementById('next-page').disabled = currentPage >= totalPages;
}

document.getElementById('prev-page').addEventListener('click', function () {
    if (currentPage > 1) {
        currentPage--;
        populateHistoryTable();
    }
});

document.getElementById('next-page').addEventListener('click', function () {
    let totalPages = Math.ceil(historyData.length / itemsPerPage);
    if (currentPage < totalPages) {
        currentPage++;
        populateHistoryTable();
    }
});
function renderPage() {
    fetchHistoryData();
    var fileInput = document.getElementById("file-upload");
    fileInput.value = "";
    var progressBar = document.getElementById("progress-bar");
    progressBar.value = 0;
}

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("btn-filtro-historico").addEventListener("click", function (event) {
        event.preventDefault();
        filtrarHistorico();
    });
});


async function filtrarHistorico() {
    let tipoOperacionalizacao = document.getElementById("tipo_operacionalizacao").value;
    let usuario = document.getElementById("usuario_historico").value;

    try {
        let response = await fetch("/historico/data");
        if (response.ok) {
            let data = await response.json();
            historyData = data.filter(item => 
                (tipoOperacionalizacao === "" || item.operation_type === tipoOperacionalizacao) &&
                (usuario === "" || item.username === usuario)
            );

            currentPage = 1;
            paginateHistory();
            renderPagination();
            limparFiltros();
        } else {
            console.error("Erro ao buscar dados do histórico.");
        }
    } catch (error) {
        console.error("Erro:", error);
    }
}

function limparFiltros() {
    document.getElementById("tipo_operacionalizacao").value = "";
    document.getElementById("usuario_historico").value = "";
}

// Função para popular os tipos de Calculos trabalhistas
/*
function CalculosTrabalhistas() {
    let moduleSelect = document.getElementById('Tipo');
    let operationTypeSelect = document.getElementById('servidor-type');
    operationTypeSelect.innerHTML = ''; // Limpa as opções atuais

    if (moduleSelect.value === 'Comissionado Exclusivo') {
        let options = ['Avos 13º', 'Férias'];
        options.forEach(option => {
            let opt = document.createElement('option');
            opt.text = option;
            opt.value = option.toLowerCase().replace(/\s+/g, '_');
            operationTypeSelect.add(opt);
        });
    } else if (moduleSelect.value === 'Prestador de Serviço/Temporario') {
        let options = ['Avos 13º'];
        options.forEach(option => {
            let opt = document.createElement('option');
            opt.text = option;
            opt.value = option.toLowerCase().replace(/\s+/g, '_');
            operationTypeSelect.add(opt);
        });
    } }
*/

 /*   
    function formatCPF(input) {
        // Remove todos os caracteres que não são números
        let value = input.value.replace(/\D/g, '');
        
        // Limita o valor a 11 dígitos
        if (value.length > 11) {
            value = value.substring(0, 11);
        }
        
        // Aplica a máscara no formato 000.000.000-00
        if (value.length > 9) {
            input.value = value.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
        } else if (value.length > 6) {
            input.value = value.replace(/(\d{3})(\d{3})(\d{3})/, '$1.$2.$3');
        } else if (value.length > 3) {
            input.value = value.replace(/(\d{3})(\d{3})/, '$1.$2');
        } else {
            input.value = value;
        }
    }
    

    function validateCPF(input) {
        const cpf = input.value.replace(/\D/g, ''); // Remove a máscara e mantém apenas os números
        let cpfError = document.getElementById("cpfError");
    
        if (cpf.length !== 11 || /^(\d)\1+$/.test(cpf)) {
            cpfError.style.display = "inline";
            return false;
        }
    
        // Validação do primeiro dígito verificador
        let sum = 0;
        for (let i = 0; i < 9; i++) {
            sum += parseInt(cpf.charAt(i)) * (10 - i);
        }
        let firstVerifier = 11 - (sum % 11);
        if (firstVerifier >= 10) firstVerifier = 0;
        if (firstVerifier !== parseInt(cpf.charAt(9))) {
            cpfError.style.display = "inline";
            return false;
        }
    
        // Validação do segundo dígito verificador
        sum = 0;
        for (let i = 0; i < 10; i++) {
            sum += parseInt(cpf.charAt(i)) * (11 - i);
        }
        let secondVerifier = 11 - (sum % 11);
        if (secondVerifier >= 10) secondVerifier = 0;
        if (secondVerifier !== parseInt(cpf.charAt(10))) {
            cpfError.style.display = "inline";
            return false;
        }
    
        // CPF válido
        cpfError.style.display = "none";
        return true;
    }
*/

function formatMatricula(input) {
    // Remove todos os caracteres que não são números ou 'x'/'X'
    let value = input.value.replace(/[^0-9xX]/g, '');

    // Limita o valor a 6 dígitos antes do hífen e um único caractere ('X' ou número) após
    if (value.length > 7) {
        value = value.substring(0, 7);
    }

    // Aplica a máscara no formato 000000-0 ou 000000-X
    if (value.length > 6) {
        // Se o último caractere é 'x' ou 'X', converte para 'X' maiúsculo
        const lastChar = value.charAt(6).toUpperCase();
        if (lastChar === 'X' || /\d/.test(lastChar)) {
            input.value = value.substring(0, 6) + '-' + lastChar;
        } else {
            input.value = value.substring(0, 6); // Remove qualquer caractere inválido
        }
    } else {
        input.value = value;
    }
}

/////////////////////////////////////////////////////
//////////// CALCULADORA////////////////////////////
////////////////////////////////////////////////////


window.onload = function () {
    alterarCampoFerias(); // Garante visibilidade correta ao carregar
    document.getElementById("tipo").addEventListener("change", alterarCampoFerias); // Atualiza ao mudar
};

document.addEventListener("DOMContentLoaded", function () {
    alterarCampoFerias(); // Garante visibilidade correta ao carregar
    document.getElementById("tipo").addEventListener("change", alterarCampoFerias); // Atualiza ao mudar
});


function alterarCampoFerias() {
    const tipo = document.getElementById("tipo").value;
    const feriasContainer = document.getElementById("ferias-container");

    if (tipo === "Comissionado Exclusivo") {
        feriasContainer.style.display = "block";
    } else {
        feriasContainer.style.display = "none";
    }
}

function calculos() {
    const checkboxRestituir = document.getElementById("dias_restituir_checkbox").checked;
    const liquido_raw = document.getElementById("liquido_calc").value;
    const dias_restituir = parseInt(document.getElementById("dias_restituir").value) || 0;

    // Captura outros campos normalmente (nome, matrícula, base, datas, etc.)
    const data = {
        nome_calc: document.getElementById("nome_calc").value,
        matricula_calc: document.getElementById("matricula_calc").value,
        cpf_calc: document.getElementById("cpf_calc").value,
        orgaos_calc: document.getElementById("orgaos_calc").value,
        tipo: document.getElementById("tipo").value,
        base_calc: parseFloat(document.getElementById("base_calc").value.replace(/\D/g, '').replace(',', '.')) || 0,
        cet_calc: parseFloat(document.getElementById("cet_calc").value.replace(/\D/g, '').replace(',', '.')) || 0,
        admissao: document.getElementById("admissao").value,
        termino: document.getElementById("termino").value,
        dias_gozados: parseInt(document.getElementById("feriasGozadas").value) || 0,
        incluir_restituicao: checkboxRestituir,
        liquido_calc: parseFloat(liquido_raw.replace(/\./g, '').replace(',', '.')) || 0,
        dias_restituir: dias_restituir
    };

    fetch('/calcular', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(resposta => {
        // construir a tabela abaixo (com ou sem campo de restituição)
        let tabela = `
            <h2>Resultado da Indenização</h2>
            <table id="processo-table" border="1">
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>Matrícula</th>
                        <th>CPF</th>
                        <th>Órgão</th>
                        <th>Tipo</th>
                        <th>Admissão</th>
                        <th>Desligamento</th>
                        <th>Dias 13°</th>
                        <th>13°</th>
                        <th>Férias Prop.</th>
                        <th>1/3 Férias</th>
                        <th>Férias Não Gozadas</th>
        `;

        if (resposta.valor_restituicao !== undefined) {
            tabela += `<th>Valor a Restituir</th>`;
        }

        tabela += `<th>Total</th></tr></thead><tbody><tr>`;
        tabela += `
            <td>${resposta.nome_calc}</td>
            <td>${resposta.matricula_calc}</td>
            <td>${resposta.cpf_calc}</td>
            <td>${resposta.orgaos_calc}</td>
            <td>${resposta.tipo}</td>
            <td>${resposta.admissao}</td>
            <td>${resposta.termino}</td>
            <td>${resposta.dias_13}</td>
            <td>R$ ${resposta.valor_13.toFixed(2)}</td>
            <td>R$ ${resposta.valor_ferias_proporcionais.toFixed(2)}</td>
            <td>R$ ${resposta.valor_terco_ferias.toFixed(2)}</td>
            <td>R$ ${resposta.valor_ferias_nao_gozadas.toFixed(2)}</td>
        `;

        if (resposta.valor_restituicao !== undefined) {
            tabela += `<td>R$ ${resposta.valor_restituicao.toFixed(2)}</td>`;
        }

        tabela += `<td><strong>R$ ${resposta.total.toFixed(2)}</strong></td></tr></tbody></table>`;
        document.getElementById("results_calculos").innerHTML = tabela;
    });
}



 
function formatMatricula(input) {
    input.value = input.value.replace(/[^0-9]/g, ''); // Permite apenas números
}

function formatDate(input) {
    let valor = input.value.replace(/\D/g, ''); // Remove tudo que não for número

    if (valor.length >= 2) {
        valor = valor.slice(0, 2) + '/' + valor.slice(2);
    }
    if (valor.length >= 5) {
        valor = valor.slice(0, 5) + '/' + valor.slice(5);
    }
    if (valor.length > 10) {
        valor = valor.slice(0, 10); // Limita a 10 caracteres (DD/MM/AAAA)
    }

    input.value = valor;
}


/*
function alterarCampoFerias() {
    const tipo = document.getElementById("Tipo").value;
    const feriasContainer = document.getElementById("ferias-container");

    if (tipo === "Comissionado Exclusivo") {
        feriasContainer.style.display = "block"; // Exibe o campo
    } else {
        feriasContainer.style.display = "none"; // Oculta o campo
        document.getElementById("feriaGozadas").value = ""; // Reseta o valor do campo
    }
}
*/
document.addEventListener("DOMContentLoaded", function () {
    const checkboxes = document.querySelectorAll(".checkbox-pago");

    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener("change", function () {
            const matricula = this.getAttribute("data-matricula");
            const status = this.checked ? "Sim" : "Não";

            fetch("/atualizar_pago", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    matricula: matricula,
                    pago: status
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data.message);
            });
        });
    });
});

//Popup tela de processos
function abrirPopup() {
    let popup = document.getElementById("popup");
    if (popup) {
        popup.style.display = "block";
    } else {
        console.error("Elemento popup não encontrado!");
    }
}

// Função para fechar o pop-up
function fecharPopupProcesso() {
    let popup = document.getElementById("popup");
    if (popup) {
        popup.style.display = "none";
    } else {
        console.error("Elemento popup não encontrado!");
    }
}

function BuscarServidor() {
    const numeroProcesso = document.getElementById("filtro-processo").value.trim();

    if (!numeroProcesso) {
        alert("Digite um número de processo!");
        return;
    }

    // Construção da URL correta para buscar apenas pelo número do processo
    let url = `/visualizar_responsavel_controle?processo=${encodeURIComponent(numeroProcesso)}`;

    console.log("Redirecionando para:", url); // Debug para ver a URL gerada
    window.location.href = url;
}


function downloadExcel(responsavel) {
    if (responsavel) {
        window.location.href = `/download_excel?responsavel=${responsavel}`;
    } else {
        alert('Responsável não especificado!');
    }
}

function editarProcesso(numeroProcesso) {
    window.location.href = `/editar_processo?numero_processo=${numeroProcesso}`;
}



// POP-UP EXCLUSÃO DE PROCESSO (controle de processo por responsável)
function mostrarPopup(numeroProcesso, responsavel) {
    var popup = document.getElementById('popup-exclusao-' + numeroProcesso);
    popup.style.display = 'block';
}

// Função para fechar o popup de exclusão
function fecharPopup(numeroProcesso) {
    // Esconder o popup específico
    var popup = document.getElementById('popup-exclusao-' + numeroProcesso);
    popup.style.display = 'none';
}


//POP-UP DE CONCLUSÃO - COMPARATIVO FOLHA
document.addEventListener("DOMContentLoaded", function () {
    const dropdownTabelasButton = document.getElementById("dropdownTabelasButton");
    const dropdownTabelasMenu = document.getElementById("dropdownTabelasMenu");
    const dropdownTabelasItems = dropdownTabelasMenu.querySelectorAll("li");
    const tabelasInput = document.getElementById("tabelas-select");
    const gerarBotao = document.getElementById("button-aba1");
    const form = document.getElementById("comparativo-form");

    // Impede envio automático ao interagir com o dropdown
    dropdownTabelasButton.addEventListener("click", function (event) {
        event.stopPropagation(); 
        dropdownTabelasMenu.classList.toggle("active");
    });

    dropdownTabelasItems.forEach(item => {
        item.addEventListener("click", function (event) {
            event.preventDefault();

            let selectedValue = this.getAttribute("data-value");

            if (selectedValue === "TODOS") {
                let allValues = Array.from(dropdownTabelasItems)
                    .map(item => item.getAttribute("data-value"))
                    .filter(value => value !== "TODOS")
                    .join(",");
                tabelasInput.value = allValues;
                dropdownTabelasButton.innerHTML = "Todas as Tabelas <i class='fas fa-chevron-down'></i>";
            } else {
                tabelasInput.value = selectedValue;
                dropdownTabelasButton.innerHTML = this.textContent + " <i class='fas fa-chevron-down'></i>";
            }

            dropdownTabelasMenu.classList.remove("active");
        });
    });

    // Fecha o dropdown se clicar fora
    document.addEventListener("click", function (event) {
        if (!dropdownTabelasButton.contains(event.target) && !dropdownTabelasMenu.contains(event.target)) {
            dropdownTabelasMenu.classList.remove("active");
        }
    });

    // Enviar o formulário SOMENTE ao clicar no botão "Gerar"
    gerarBotao.addEventListener("click", function (event) {
        event.preventDefault();

        // Verificar se há tabelas selecionadas
        if (!tabelasInput.value.trim()) {
            alert("Por favor, selecione uma tabela antes de gerar o comparativo.");
            return;
        }

        let formData = new FormData(form);

        fetch('/comparativo_folha', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Erro ao gerar o arquivo.");
            }
            return response.blob();
        })
        .then(blob => {
            let url = window.URL.createObjectURL(blob);
            let a = document.createElement("a");
            a.href = url;
            a.download = "Comparativo_Folha.csv"; 
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);

            exibirPopup("Comparativo concluído com sucesso!");
        })
        .catch(error => {
            alert("Erro: " + error.message);
        });
    });
});

// Função para exibir o popup
function exibirPopup(mensagem) {
    let popup = document.getElementById('popup');
    let label = popup.querySelector('.bold-label');
    label.innerText = mensagem;
    popup.style.display = 'block';

    setTimeout(() => fecharPopupProcesso(), 5000);
}

// Função para fechar o popup
function fecharPopupProcesso() {
    document.getElementById('popup').style.display = 'none';
}




//FUNÇÃO PARA LOGOUT
function logoutUser() {
    fetch("{{ url_for('logout') }}", {
        method: "POST"
    }).then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    const dropdownButton = document.querySelector(".dropdown-button");
    const dropdownMenu = document.querySelector(".dropdown-menu");
    const dropdownItems = document.querySelectorAll(".dropdown-menu li");

    // Abrir/Fechar dropdown ao clicar
    dropdownButton.addEventListener("click", function () {
        dropdownMenu.classList.toggle("active");
    });

    // Seleciona um item e fecha o menu
    dropdownItems.forEach(item => {
        item.addEventListener("click", function () {
            dropdownButton.innerHTML = this.textContent + ' <i class="fas fa-chevron-down"></i>';
            dropdownMenu.classList.remove("active");
        });
    });

    // Fecha o dropdown ao clicar fora dele
    document.addEventListener("click", function (event) {
        if (!document.querySelector(".dropdown-container").contains(event.target)) {
            dropdownMenu.classList.remove("active");
        }
    });
});

function addDropdown() {
    const container = document.getElementById('tipo-container');
    const newSelect = document.createElement('select');
    newSelect.name = 'tipo[]';
    newSelect.innerHTML = `<!-- Copie todas as opções do dropdown original aqui -->`;
    container.appendChild(newSelect);
    container.appendChild(document.createElement('br'));
}


document.querySelectorAll('.input-moeda').forEach(input => {
    input.addEventListener('input', formatarMoeda);
    });
    
    function formatarMoeda(event) {
        let valor = event.target.value.replace(/\D/g, ''); // Remove tudo que não é dígito
        valor = (valor / 100).toFixed(2) + ''; // Divide por 100 e formata com duas casas decimais
        valor = valor.replace('.', ','); // Troca ponto por vírgula
        event.target.value = valor; // Atualiza o campo com o valor formatado
    }
    document.addEventListener('DOMContentLoaded', function() {
        var messagesContainer = document.getElementById('flash-messages');
        var messages = messagesContainer.querySelectorAll('div');
        messages.forEach(function(msg) {
            alert(msg.textContent); // Exibe cada mensagem em um pop-up
        });
    });

