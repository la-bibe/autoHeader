(setq autoheader-highlights
      '(("[a-zA-Z]*:.*;" . font-lock-builtin-face)
	("!?[_a-zA-Z0-9\.\/]*:" . font-lock-type-face)
	("[ \t]*[\-_a-zA-Z0-9]*;" . font-lock-function-name-face)
        ("-?=?" . font-lock-keyword-face)
	))

(define-derived-mode autoheader-mode fundamental-mode "autoheader"
  "Major mode for editing .conf files."
  (global-set-key (kbd "C-<down>") 'autoheader-mode-move-next)
  (global-set-key (kbd "C-<up>") 'autoheader-mode-move-prev)

  (defun autoheader-mode-move-next ()
    (interactive)
    (re-search-forward "!?[_a-zA-Z0-9\.\/]*:$"))
  (defun autoheader-mode-move-prev ()
    (interactive)
    (search-backward-regexp "!?[_a-zA-Z0-9\.\/]*:$"))
  (setq font-lock-defaults '(autoheader-highlights)))
