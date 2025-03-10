import 'package:flutter/material.dart';
import '../../../core/models/capabilities_model.dart';
import '../widgets/capabilities_form.dart';

class CapabilitiesPage extends StatefulWidget {
  final CapabilitiesModel? initialCapabilities;

  const CapabilitiesPage({
    Key? key,
    this.initialCapabilities,
  }) : super(key: key);

  @override
  _CapabilitiesPageState createState() => _CapabilitiesPageState();
}

class _CapabilitiesPageState extends State<CapabilitiesPage> {
  final _formKey = GlobalKey<FormState>();
  late CapabilitiesModel _capabilities;

  @override
  void initState() {
    super.initState();
    _capabilities = widget.initialCapabilities ?? CapabilitiesModel();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('配置 Capabilities'),
        actions: [
          IconButton(
            icon: Icon(Icons.refresh),
            onPressed: _resetCapabilities,
            tooltip: '重置',
          ),
          TextButton(
            onPressed: _saveCapabilities,
            child: Text('保存'),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16.0),
        child: CapabilitiesForm(
          formKey: _formKey,
          capabilities: _capabilities,
          onChanged: (value) => setState(() => _capabilities = value),
        ),
      ),
    );
  } 

  void _resetCapabilities() {
    setState(() {
      _capabilities = CapabilitiesModel();
    });
  }

  void _saveCapabilities() {
    if (_formKey.currentState?.validate() ?? false) {
      Navigator.pop(context, _capabilities);
    }
  }
}