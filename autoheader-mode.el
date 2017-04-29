(setq autoheader-highlights
      '(("[a-zA-Z]*:.*;" . font-lock-builtin-face)
	("!?[_a-zA-Z0-9\.\/]*:" . font-lock-type-face)
	("[ \t]*[\-_a-zA-Z0-9]*;" . font-lock-function-name-face)
        ("-?=?" . font-lock-keyword-face)
	))

(global-set-key (kbd "C-<down>") 'autoheader-move-next)
(global-set-key (kbd "C-<up>") 'autoheader-move-prev)

(defun autoheader-move-next ()
  (interactive)
  (re-search-forward "!?[_a-zA-Z0-9\.\/]*:$"))
(defun autoheader-move-prev ()
  (interactive)
  (search-backward-regexp "!?[_a-zA-Z0-9\.\/]*:$"))

(define-derived-mode autoheader-mode fundamental-mode "autoheader"
  "Major mode for editing .conf files."
  (setq font-lock-defaults '(autoheader-highlights)))
