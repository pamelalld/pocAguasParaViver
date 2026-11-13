/* Águas para Viver — comportamentos compartilhados do front */
(function () {
  "use strict";

  // Mostrar/ocultar senha
  document.querySelectorAll("[data-alternar-senha]").forEach(function (botao) {
    var campo = document.getElementById(botao.getAttribute("data-alternar-senha"));
    if (!campo) return;
    var iconeVer = botao.querySelector("[data-icone='ver']");
    var iconeOcultar = botao.querySelector("[data-icone='ocultar']");
    botao.addEventListener("click", function () {
      var mostrar = campo.type === "password";
      campo.type = mostrar ? "text" : "password";
      botao.setAttribute("aria-label", mostrar ? "Ocultar senha" : "Mostrar senha");
      botao.setAttribute("aria-pressed", mostrar ? "true" : "false");
      if (iconeVer) iconeVer.hidden = !mostrar;
      if (iconeOcultar) iconeOcultar.hidden = mostrar;
    });
  });

  // Confirmação de senha (cadastro)
  var confirmar = document.getElementById("confirmarSenha");
  var senha = document.getElementById("senha");
  if (confirmar && senha) {
    var validar = function () {
      confirmar.setCustomValidity(
        confirmar.value && confirmar.value !== senha.value ? "As senhas não coincidem." : ""
      );
    };
    senha.addEventListener("input", validar);
    confirmar.addEventListener("input", validar);
  }

  // Campos que começam somente leitura e são liberados pelo botão de lápis
  document.querySelectorAll("[data-somente-leitura]").forEach(function (campo) {
    campo.setAttribute("readonly", "");
    // Enquanto bloqueado, o campo se ajusta ao texto para não cortar a descrição
    campo.style.height = "auto";
    campo.style.height = (campo.scrollHeight + 4) + "px";
  });
  document.querySelectorAll("[data-liberar]").forEach(function (botao) {
    botao.addEventListener("click", function () {
      var campo = document.getElementById(botao.getAttribute("data-liberar"));
      if (!campo) return;
      campo.removeAttribute("readonly");
      campo.style.height = "";
      campo.focus();
    });
  });

  // Prévia da nova imagem escolhida
  document.querySelectorAll("[data-previa]").forEach(function (input) {
    var img = document.getElementById(input.getAttribute("data-previa"));
    if (!img) return;
    input.addEventListener("change", function () {
      var arquivo = input.files && input.files[0];
      if (arquivo) img.src = URL.createObjectURL(arquivo);
    });
  });

    // Carrossel automático de imagens
// Carrossel automático de imagens
document.querySelectorAll(".carrossel").forEach(function (carrossel) {
  var imagens = carrossel.querySelectorAll("img");

  if (imagens.length <= 1) return;

  var atual = 0;

  setInterval(function () {
    atual++;

    // Se chegou ao final, volta instantaneamente ao início
    if (atual >= imagens.length) {
      atual = 0;

      carrossel.scrollTo({
        left: 0,
        behavior: "instant"
      });

    } else {
      // Continua avançando suavemente
      carrossel.scrollTo({
        left: imagens[atual].offsetLeft - imagens[0].offsetLeft,
        behavior: "smooth"
      });
    }

    }, 1000);
  });

  // Confirmação personalizada de exclusão de nascente
  var botaoInvalidar = document.getElementById("botaoInvalidar");
  var modalExclusao = document.getElementById("confirmarExclusao");
  var cancelarExclusao = document.getElementById("cancelarExclusao");
  var confirmarExclusao = document.getElementById("confirmarExclusaoBtn");

  if (botaoInvalidar && modalExclusao) {

    botaoInvalidar.addEventListener("click", function (event) {
      event.preventDefault();
      modalExclusao.showModal();
    });

    cancelarExclusao.addEventListener("click", function () {
      modalExclusao.close();
    });

    confirmarExclusao.addEventListener("click", function () {
      modalExclusao.close();

      // Envia o formulário com a ação de invalidar
      botaoInvalidar.form.requestSubmit(botaoInvalidar);
    });
  }
})();
