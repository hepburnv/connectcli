#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'yuyuan yue'

import sys,os,json
from common import connectool
from connectapi import ConnectApi
import click

@click.group()
@click.option('-k','--apikey','apikey',metavar='',help='app store connect api key',required=True)
@click.option('-i','--issuer','issuer_id',metavar='',help='app store connect issuer id',required=True)
@click.option('-p','--privatekey_path','privatekey_path',type=click.Path(exists=True),metavar='',help='privatekey file path , default linux user root path ".private_keys"')
@click.pass_context
def cli(ctx, apikey, issuer_id,privatekey_path):
    '''
    app store connect api cli with python use apikey private_key and issuer_id to authorize
    
    how to get apikey,private_key and issuer_id ? https://developer.apple.com/documentation/appstoreconnectapi
    '''
    
    if privatekey_path:
        if apikey in privatekey_path:
            ctx.obj = ConnectApi(apikey,issuer_id,privatekey_path)
        else:
            connectool.raiseError('private key path error apikey '+apikey+' not in '+privatekey_path)
    else:
        ctx.obj = ConnectApi(apikey,issuer_id,privatekey_path)
    

@click.command()
@click.option('-n','--name','name',metavar='',help='device name',required=True)
@click.option('-u','--udid','udid',metavar='',help='device udid',required=True)
@click.pass_obj
def registerdevice(api,name,udid):
    '''register device into app store connect with name and udid '''
    result = api.register_device(name,udid)
    click.echo(json.dumps(result))
    return result

@click.command()
@click.option('-l','--limit','limit',default=100,metavar='', help='the devices count,default 100')
@click.option('-s','--sort','sort',default='id',metavar='',help='the devices sort,default id')
@click.pass_obj
def devices(api,limit,sort):
    '''list devices with limit and sort '''
    result = api.list_devices(limit,sort)
    click.echo(json.dumps(result))
    return result

@click.command()
@click.option('-c','--csr_path','csr_path',type=click.Path(exists=True),metavar='',help='certificare csr request file path,must value',required=True)
@click.option('-o','--out','out_path',type=click.Path(exists=True),default=lambda: os.environ.get('HOME', ''),metavar='',help='certificate file out path , default user root path')
@click.option('-t','--type','type',type=click.Choice(['IOS_DEVELOPMENT','IOS_DISTRIBUTION']),default='IOS_DEVELOPMENT',metavar='',help='the certificate type,choice:[IOS_DEVELOPMENT,IOS_DISTRIBUTION] default IOS_DEVELOPMENT')
@click.pass_obj
def registercertificate(api,csr_path,out_path,type):
    '''register certificate with csr_path,out_path and type'''
    result = api.register_certificate(csr_path=csr_path,out_path=out_path,type=type)
    click.echo(json.dumps(result))
    return result

@click.command()
@click.option('-i','--id','id',metavar='', help='the certificate id',required=True)
@click.pass_obj
def deletecertificate(api,id):
    '''delete certificate with id '''
    result = api.delete_certificate(id)
    click.echo(json.dumps(result))
    return result

@click.command()
@click.option('-l','--limit','limit',default=100,metavar='', help='the certificates count,default 100')
@click.option('-s','--sort','sort',default='id',metavar='',help='the certificates sort,default id')
@click.pass_obj
def certificates(api,limit,sort):
    '''list certificate with limit and sort '''
    result = api.list_certificates(limit,sort)
    click.echo(json.dumps(result))
    return result

@click.command()
@click.option('-b','--bundleid','bundleid',metavar='',help='bundle id',required=True)
@click.option('-t','--teamid','teamid',metavar='',help='team id',required=True)
@click.option('-n','--name','name',metavar='',help='bunle id name',required=True)
@click.pass_obj
def registerbundleid(api,bundleid,teamid,name):
    '''register bundle id into app store connect with bundle_id team_id and name '''
    result = api.register_bundle_id(bundleid,teamid,name)
    click.echo(json.dumps(result))
    return result

@click.command()
@click.option('-l','--limit','limit',default=100,metavar='', help='the bundleid count,default 100')
@click.option('-s','--sort','sort',default='id',metavar='',help='the bundleid sort,default id')
@click.pass_obj
def bundleids(api,limit,sort):
    '''list bundleids with limit and sort '''
    result = api.list_bundle_ids(limit,sort)
    click.echo(json.dumps(result))
    return result

@click.command()
@click.option('-i','--id','id',metavar='', help='the bundleid id',required=True)
@click.pass_obj
def deletebundleid(api,id):
    '''delete bundleid with id '''
    result = api.delete_bundle_id(id)
    click.echo(json.dumps(result))
    return result

@click.command()
@click.option('-i','--id','id',metavar='', help='the bundleid id',required=True)
@click.pass_obj
def getbundleid(api,id):
    '''get bundleid with id '''
    result = api.get_bundle_id(id)
    click.echo(json.dumps(result))
    return result

@click.command()
@click.option('-i','--id','id',metavar='', help='the bundleid id',required=True)
@click.pass_obj
def getbundleidprofiles(api,id):
    '''get bundleid profiles with id '''
    result = api.get_bundle_id_profiles(id)
    click.echo(json.dumps(result))
    return result

@click.command()
@click.option('-a', '--app_id', 'app_id', metavar='', help='App id', required=True)
@click.option('-v', '--version_string', 'version_string', metavar='', help='Version like "1.0.0"', required=True)
@click.option('-p', '--platform', 'platform', metavar='', 
                help='App platform. Choice IOS, MAC_OS or TV_OS. Default IOS',
                type=click.Choice(['IOS','MAC_OS','TV_OS']), default='IOS')
@click.option('-r', '--release_type', 'release_type', metavar='', 
                help='Type of release after app is approved. Choice MANUAL, AFTER_APPROVAL or SCHEDULED. Default MANUAL',
                type=click.Choice(['MANUAL','AFTER_APPROVAL','SCHEDULED']), default='MANUAL')
@click.option('-c', '--copyright', 'copyright', metavar='', help='Proprietary company or person', default='None')
@click.option('-b', '--build_id', 'build_id', metavar='', help='Build id related to the version', default='None')
@click.option('-e', '--earliest_release_date', 'earliest_release_date', help='Date-time for scheduled release', default='None')
@click.option('-u', '--uses_idfa', 'uses_idfa', metavar='', help='If app uses IDFA', default='False')
@click.pass_obj
def createappversion(api, app_id, version_string, platform, release_type, copyright, build_id, earliest_release_date, uses_idfa):
    '''create app store version with app_id, version_string, platform, release_type, copyright, build_id, earliest_release_date and uses_idfa'''
    result = api.createappversion(app_id=app_id, version_string=version_string, platform=platform, 
                                    release_type=release_type, copyright=copyright, build_id=build_id, 
                                    earliest_release_date=earliest_release_date, uses_idfa=uses_idfa) 
    click.echo(json.dumps(result))
    return result

@click.command()
@click.option('-i', '--id', 'id', metavar='', help='the app version id', required=True)
@click.pass_obj
def getappversionlocalizations(api,id):
    '''get app version localized info with id '''
    result = api.get_app_version_localizations(id)
    click.echo(json.dumps(result))
    return result

@click.command()
@click.option('-n','--name','name',metavar='',help='profile name',required=True)
@click.option('-b','--bundleid','bundleid',metavar='',help='profile contact bundleid id',required=True)
@click.option('-c','--certificate','certificate',metavar='',help='profile contact certificate id',required=True)
@click.option('-o','--out','out_path',type=click.Path(exists=True),default=lambda: os.environ.get('HOME', ''),metavar='',help='profile file out path , default user root path')
@click.option('-t','--type','type',type=click.Choice(['IOS_APP_DEVELOPMENT','IOS_APP_STORE','IOS_APP_ADHOC']),default='IOS_DEVELOPMENT',metavar='',help='the certificate type,choice:[IOS_APP_DEVELOPMENT, IOS_APP_STORE, IOS_APP_ADHOC] default IOS_APP_ADHOC')
@click.pass_obj
def createprofile(api,name,bundleid,certificateid,out_path,type):
    '''create profile with name,bundleid,certificateid,out_path and type'''
    result = api.create_profile(name=name,bundle_id=bundleid,certificate_id=certificateid,out_path=out_path,type=type)
    click.echo(json.dumps(result))
    return result

@click.command()
@click.option('-i','--id','id',metavar='', help='the profile id',required=True)
@click.pass_obj
def deleteprofile(api,id):
    '''delete profile with id '''
    result = api.delete_profile(id)
    click.echo(json.dumps(result))
    return result

@click.command()
@click.option('-l','--limit','limit',default=100,metavar='', help='the profiles count,default 100')
@click.option('-s','--sort','sort',default='id',metavar='',help='the profiles sort,default id')
@click.pass_obj
def profiles(api,limit,sort):
    '''list profiles with limit and sort '''
    result = api.list_profiles(limit,sort)
    click.echo(json.dumps(result))
    return result

@click.command()
@click.option('-i','--id','id',metavar='', help='the profile id',required=True)
@click.pass_obj
def requestprofile(api,id):
    '''request profile with id '''
    result = api.request_profile(id)
    click.echo(json.dumps(result))
    return result

@click.command()
@click.option('-o','--out','outpath',type=click.Path(exists=True),default=lambda: os.environ.get('HOME', ''),metavar='',help='file out path , default user root path')
@click.option('-l','--limit','limit',default=100,metavar='', help='the certificates count,default 100')
@click.option('-s','--sort','sort',default='id',metavar='',help='the certificates sort,default id')
@click.pass_obj
def downloadcerts(api,outpath,limit,sort):
    '''download certificate with limit and sort '''
    result = api.download_certificates(outpath,limit,sort)
    click.echo(json.dumps(result))
    return result

@click.option('-o','--out','outpath',type=click.Path(exists=True),default=lambda: os.environ.get('HOME', ''),metavar='',help='file out path , default user root path')
@click.option('-l','--limit','limit',default=100,metavar='', help='the profiles count,default 100')
@click.option('-s','--sort','sort',default='id',metavar='',help='the profiles sort,default id')
@click.pass_obj
def downloadprofiles(api,outpath,limit,sort):
    '''download profile with limit and sort '''
    result = api.download_profiles(outpath,limit,sort)
    click.echo(json.dumps(result))
    return result

@click.command()
@click.option('-l', '--limit', 'limit', default=100, metavar='', help='the apps count, default 100')
@click.option('-s', '--sort', 'sort', default='bundleId', metavar='', help='the apps sort, default bundleId')
@click.option('-b', '--bundleId', 'bundleId', default='None', metavar='', help='the bundle ID to filter, default None')
@click.pass_obj
def apps(api, limit, sort, filter_bundle_id):
    '''list apps with limit, sort and filter '''
    result = api.list_apps(limit, sort, filter_bundle_id)
    click.echo(json.dumps(result))
    return result

@click.command()
@click.option('-i', '--id', 'id', metavar='', help='the app id', required=True)
@click.pass_obj
def getappversions(api, id):
    '''get app versions with id '''
    result = api.get_app_versions(id)
    click.echo(json.dumps(result))
    return result

cli.add_command(registerdevice)
cli.add_command(devices)

cli.add_command(registercertificate)
cli.add_command(deletecertificate)
cli.add_command(certificates)
cli.add_command(downloadcerts)

cli.add_command(createappversion)
cli.add_command(getappversionlocalizations)

cli.add_command(registerbundleid)
cli.add_command(bundleids)
cli.add_command(deletebundleid)
cli.add_command(getbundleid)
cli.add_command(getbundleidprofiles)

cli.add_command(createprofile)
cli.add_command(deleteprofile)
cli.add_command(profiles)
cli.add_command(requestprofile)
cli.add_command(downloadprofiles)

cli.add_command(apps)
cli.add_command(getappversions)



if __name__ == '__main__':
    cli()
    api = ConnectApi('T5VR6D3TZY','5127e6a3-99ef-458f-9ea3-ba6b76e9cc13')
    
    devices = api.list_devices(limit=1)
    print(devices)
    
    result = api.register_device('test','test')
    print(result)
    
    result = api.register_certificate(csr_path='/Users/last/Desktop/CertificateSigningRequest.certSigningRequest')
    print(result)
    
    result = api.delete_certificate('N9P79WJTHK')
    print(result)
    
    result = api.list_certificates()
    print(result)
    
    result = api.register_bundle_id(bundle_id='com.hepburn.app',team_id='6DD349HLLU',name='hepburn')
    print(result)
    
    result = api.list_bundle_ids()
    print(result)
    
    result = api.get_bundle_id('N49MX9AWAX')
    print(result)
    
    result = api.get_bundle_id_profiles('N49MX9AWAX')
    print(result)
    
    result = api.delete_bundle_id('N49MX9AWAX')
    print(result)

    result = api.create_app_version(app_id='123456', version_string='1.2.3', platform='IOS', 
                                    release_type='AFTER_APPROVAL', copyright='2020 My Company', build_id='123', 
                                    earliest_release_date=None, uses_idfa=False)
    print(result)
    
    result = api.get_app_version_localizations('a1a2a3a4-a1a2-a1a2-a1a2-a1a2a3a4a5a6')
    print(result)
    
    result = api.create_profile(name='adhoc1',bundle_id='VSLGJ82UHW',certificate_id='T553J666XW',type='IOS_APP_DEVELOPMENT')
    print(result)
    
    result = api.delete_profile('4KVXW4LK52')
    print(result)
    
    result = api.list_profiles()
    print(result)
    
    result = api.request_profile('4KVXW4LK52')
    print(result)
    
    result = api.list_apps()
    print(result)
    
    result = api.get_app_versions('123456')
    print(result)