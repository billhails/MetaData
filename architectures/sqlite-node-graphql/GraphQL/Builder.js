/*
 * no-op function allowing an override by `--extra` templates
 */
function build(catalogue) {
    return catalogue;
}

module.exports = { build };